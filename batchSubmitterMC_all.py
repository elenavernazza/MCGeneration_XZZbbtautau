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

    resubmitting = []
    done = []
    running = []

    starting_index = int(options.start_from)
    ending_index = starting_index + int(options.nJobs)
    print(" ### INFO: Index range", starting_index, ending_index)
    os.system('mkdir -p '+outdir+'/jobs')
    for idx in range(starting_index, ending_index):

        os.system('mkdir -p '+outdir+'/jobs/' + str(idx))
        outJobName  = outdir + '/jobs/' + str(idx) + '/job_' + str(idx) + '.sh'

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

        # if options.resubmit:
        #     LogJobName = outdir + '/jobs/' + str(idx) + '/log_' + str(idx) + '.txt'
        #     ListErrJobName = glob.glob(outdir + '/jobs/' + str(idx) + '/job_' + str(idx) + '.sh.e*')
        #     ListOutJobName = glob.glob(outdir + '/jobs/' + str(idx) + '/job_' + str(idx) + '.sh.o*')
        #     if os.path.isfile(LogJobName):
        #         if len(os.popen('tail '+LogJobName+' | grep dropped').read()) > 0 or len(os.popen('grep "2000th" '+LogJobName).read()) > 0:
        #             done.append(idx)
        #             continue

        #         if len(ListErrJobName) > 0:
        #             if len(os.popen('grep "Begin Fatal Exception" '+LogJobName).read()) > 0 or len(open(ListErrJobName[-1]).readlines()) > 0:
        #                 if len(open(ListErrJobName[-1]).readlines()) > 0:
        #                     print('\n ### INFO: Job', str(idx) , 'failed due to error', open(ListErrJobName[-1]).readlines())
        #                 print(' ### INFO: Resubmitting job ' + str(idx))
        #                 if not options.no_exec:
        #                     os.system('rm '+ListErrJobName[-1])
        #                     os.system('rm '+ListOutJobName[-1])
        #                 resubmitting.append(idx)
        #         else:
        #             running.append(idx)
        #             continue

        #     else:
        #         print(" ### INFO: Log file not existing yet")


        skimjob = open (outJobName, 'w')
        skimjob.write ('#!/bin/bash\n')
        skimjob.write ('export X509_USER_PROXY=~/.t3/proxy.cert\n')
        skimjob.write ('source /cvmfs/cms.cern.ch/cmsset_default.sh\n')
        for cmsRun in cmsRuns:
            skimjob.write(cmsRun)
        skimjob.close ()

        os.system ('chmod u+rwx ' + outJobName)
        command = ('/home/llr/cms/evernazza/t3submit -'+options.queue+' \'' + outJobName +"\'")
        print(command)
        if not options.no_exec: os.system (command)

    # if options.resubmit:
    #     if len(running) > 0:
    #         print(" ### BE PATIENT! "+str(len(running))+" job(s) still running ...")
    #         print(running, "\n")
    #     else:
    #         if len(done) == int(options.nJobs):
    #             print(" ### CONGRATULATION! EVERYTHING IS DONE! :)\n")
    #         else:
    #             print(" ### ALL JOBS DONE!\n")