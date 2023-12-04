import os, glob, sys
from datetime import datetime
from optparse import OptionParser

conf_dict = [
    {
      "release": "CMSSW_10_6_18",
      "cfg": "gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_0_cfg.py",
      "KeepOutput": False,
    },
    {
      "release": "CMSSW_10_6_17_patch1",
      "cfg": "gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_1_cfg.py",
      "KeepOutput": False,
    },
    {
      "release": "CMSSW_10_2_16_UL",
      "cfg": "gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_2_cfg.py",
      "KeepOutput": False,
    },
    {
      "release": "CMSSW_10_6_17_patch1",
      "cfg": "gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_3_cfg.py",
      "KeepOutput": True,
    },
    {
      "release": "CMSSW_10_6_19_patch2",
      "cfg": "gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_4_cfg.py",
      "KeepOutput": False,
    }
]

# Script to submit MC production

if __name__ == "__main__" :

    parser = OptionParser()    
    parser.add_option("--base",      dest="base",      type=str,            default=None,                            help="Base output folder name")
    parser.add_option("--grid",      dest="grid",      type=str,            default=None,                            help="Gridpack location for step 0")
    parser.add_option("--maxEvents", dest="maxEvents", type=int,            default=50,                              help="Number of events per job")
    parser.add_option("--nJobs",     dest="nJobs",     type=int,            default=1,                               help="Number of jobs")
    parser.add_option("--start_from",dest="start_from",type=int,            default=0,                               help="Start random seed from")
    parser.add_option("--queue",     dest="queue",     type=str,            default='short',                         help="long or short queue")
    parser.add_option("--no_exec",   dest="no_exec",   action='store_true', default=False)
    parser.add_option("--resubmit",  dest="resubmit",  action='store_true', default=False)
    (options, args) = parser.parse_args()

    outdir = options.base
    print(" ### INFO: Saving output in", outdir)
    os.system('mkdir -p '+outdir)

    if options.grid == None:
        sys.exit(" ### ERROR: Specify gridpack location")
    print(" ### INFO: Gridpack location is", options.grid)

    starting_index = int(options.start_from)
    ending_index = starting_index + int(options.nJobs)
    print(" ### INFO: Index range", starting_index, ending_index)
    os.system('mkdir -p '+outdir+'/jobs')

    status = {i: -1 for i in range(starting_index, ending_index)}

    for idx in range(starting_index, ending_index):
        
        resubmit = False

        os.system('mkdir -p '+outdir+'/jobs/' + str(idx))
        outJobName  = outdir + '/jobs/' + str(idx) + '/job_' + str(idx) + '.sh'
        # if options.resubmit: outJobName = outdir + '/jobs/' + str(idx) + '/job_' + str(idx) + '_re.sh'

        # random seed for MC production should every time we submit a new generation
        # it's obtained by summing current Y+M+D+H+M+S+job_number
        # now = datetime.now()
        # randseed = int(now.year) + int(now.month) + int(now.day) + int(now.hour) + int(now.minute) + int(now.second) + idx
        randseed = idx+1 # to be reproducible

        cmsRuns = []

        for step in range(len(conf_dict)):
            
            cur_dir = outdir + '/Step_' + str(step)
            os.system('mkdir -p '+cur_dir)
            outRootName = cur_dir + '/Ntuple_' + str(idx) + '.root'
            if step > 0:
                prev_dir = outdir + '/Step_' + str(step-1)
                inRootName = prev_dir + '/Ntuple_' + str(idx) + '_numEvent' + str(options.maxEvents) + '.root'
            outLogName  = outdir + '/jobs/' + str(idx) + '/log_' + str(step) + '_' + str(idx) + '.txt'

            if options.resubmit:
                if not resubmit:
                  if os.path.isfile(outLogName):
                      if len(os.popen('tail '+outLogName+' | grep dropped').read()) > 0:
                          status[idx] = step
                          continue
                      elif len(os.popen('grep "Fatal" '+outLogName).read()) > 0 or len(os.popen('grep "fatal" '+outLogName).read()) > 0:
                          resubmit = True
                          if not "Error" in str(status[idx]):
                            status[idx] = "Error Step%s" %(str(step))
                  else:
                      continue # not started yet

            cfg = conf_dict[step]['cfg']
            release = conf_dict[step]['release']
            cmsRun = 'cd /data_CMS/cms/vernazza/MCProduction/2023_11_14/%s/src\n' %release
            cmsRun += 'cmsenv\n'
            cmsRun += 'eval `scram r -sh`\n'
            cmsRun += 'cd %s\n' %(outdir + '/jobs/' + str(idx))
            cmsRun += "cmsRun " + os.getcwd() + "/" + cfg + " outputFile=file:"+outRootName + \
                " maxEvents="+str(options.maxEvents)+" randseed="+str(randseed)
            if step == 0: cmsRun = cmsRun+" inputFiles="+options.grid
            if int(step) > 0: cmsRun = cmsRun+" inputFiles=file:"+inRootName
            cmsRun += " >& "+outLogName + '\n'
            if int(step) > 0:
                keep = conf_dict[int(step-1)]['KeepOutput']
                if not keep: cmsRun += "rm "+inRootName + '\n'
            cmsRuns.append(cmsRun)

        if not options.resubmit:
            skimjob = open (outJobName, 'w')
            skimjob.write ('#!/bin/bash\n')
            skimjob.write ('export X509_USER_PROXY=~/.t3/proxy.cert\n')
            skimjob.write ('source /cvmfs/cms.cern.ch/cmsset_default.sh\n')
            for cmsRun in cmsRuns:
                skimjob.write(cmsRun)
            skimjob.close ()

            os.system ('chmod u+rwx ' + outJobName)
        
        if options.resubmit:
            if not resubmit: continue
            if not options.no_exec: os.system ('rm ' + outdir + '/jobs/' + str(idx) + '/log_*')

        # command = ('/home/llr/cms/evernazza/t3submit -'+options.queue+' \'' + outJobName +"\'")
        command = ('/opt/exp_soft/cms/t3/t3submit -8c -reserv -'+options.queue+' \'' + outJobName +"\'")
        print(command)
        if not options.no_exec: os.system (command)


    if options.resubmit:
        done = [i for i in status.keys() if status[i] == 4]
        if len(done) == int(options.nJobs):
            print(" ### CONGRATULATION! EVERYTHING IS DONE! :)\n")
        else:
            error = [i for i in status.keys() if "Error" in str(status[i])]
            print(" ### JOBS RESUBMITTED: {}\n".format(error))
            running_0 = [i for i in status.keys() if status[i] == -1]
            running_1 = [i for i in status.keys() if status[i] == 0]
            running_2 = [i for i in status.keys() if status[i] == 1]
            running_3 = [i for i in status.keys() if status[i] == 2]
            running_4 = [i for i in status.keys() if status[i] == 3]
            print(" ### INFO: Running Step 0", running_0)
            print(" ### INFO: Running Step 1", running_1)
            print(" ### INFO: Running Step 2", running_2)
            print(" ### INFO: Running Step 3", running_3)
            print(" ### INFO: Running Step 4", running_4)
            print(" ### INFO: Done", done)
