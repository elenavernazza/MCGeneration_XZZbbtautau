import os, glob, sys
from datetime import datetime
from optparse import OptionParser

# Script to submit MC production

if __name__ == "__main__" :

    parser = OptionParser()    
    parser.add_option("--step",      dest="step",      type=str,            default="0",                             help="Step number")
    parser.add_option("--cfg",       dest="cfg",       type=str,            default="Step_0_cfg.py",                 help="Config file")
    parser.add_option("--cmssw",     dest="cmssw",     type=str,            default="./CMSSW_10_6_18",               help="Path to CMSSW release")
    parser.add_option("--base",      dest="base",      type=str,            default=None,                            help="Base output folder name")
    parser.add_option("--grid",      dest="grid",      type=str,            default=None,                            help="Gridpack location for step 0")
    parser.add_option("--maxEvents", dest="maxEvents", type=int,            default=50,                              help="Number of events per job")
    parser.add_option("--nJobs",     dest="nJobs",     type=int,            default=1,                               help="Number of jobs")
    parser.add_option("--start_from",dest="start_from",type=int,            default=0,                               help="Start random seed from")
    parser.add_option("--queue",     dest="queue",     type=str,            default='short',                         help="long or short queue")
    parser.add_option("--no_exec",   dest="no_exec",   action='store_true', default=False)
    parser.add_option("--resubmit",  dest="resubmit",  action='store_true', default=False)
    (options, args) = parser.parse_args()

    outdir = options.base + "/Step" + options.step
    print(" ### INFO: Saving output in", outdir)
    os.system('mkdir -p '+outdir)

    if int(options.step) == 0:
        if options.grid == None:
            sys.exit(" ### ERROR: Specify gridpack location")
        print(" ### INFO: Gridpack location is", options.grid)

    if int(options.step) > 0:
        prev_outdir = options.base + "/Step" + str(int(options.step) - 1)
        print(" ### INFO: Previous step folder", prev_outdir)

    resubmitting = 0

    starting_index = int(options.start_from)
    ending_index = starting_index + int(options.nJobs)
    print(" ### INFO: Index range", starting_index, ending_index)
    os.system('mkdir -p '+outdir+'/jobs')
    for idx in range(starting_index, ending_index):

        os.system('mkdir -p '+outdir+'/jobs/' + str(idx))
        outJobName  = outdir + '/jobs/' + str(idx) + '/job_' + str(idx) + '.sh'
        outLogName  = outdir + '/jobs/' + str(idx) + '/log_' + str(idx) + '.txt'
        outRootName = outdir + '/Ntuple_' + str(idx) + '.root'
        if int(options.step) > 0: inRootName = prev_outdir + '/Ntuple_' + str(idx) + '_numEvent' + str(options.maxEvents) + '.root'

        # random seed for MC production should every time we submit a new generation
        # it's obtained by summing current Y+M+D+H+M+S+job_number
        # now = datetime.now()
        # randseed = int(now.year) + int(now.month) + int(now.day) + int(now.hour) + int(now.minute) + int(now.second) + idx
        randseed = idx+1 # to be reproducible

        if options.resubmit:
            LogJobName = outdir + '/jobs/' + str(idx) + '/log_' + str(idx) + '.txt'
            ListErrJobName = glob.glob(outdir + '/jobs/' + str(idx) + '/job_' + str(idx) + '.sh.e*')
            ListOutJobName = glob.glob(outdir + '/jobs/' + str(idx) + '/job_' + str(idx) + '.sh.o*')
            if len(ListErrJobName) > 0:
                if len(os.popen('grep "Begin Fatal Exception" '+LogJobName).read()) > 0 or len(open(ListErrJobName[0]).readlines()) > 0:
                    if len(open(ListErrJobName[0]).readlines()) > 0:
                        print(' ### INFO: Job failed due to error\n', open(ListErrJobName[0]).readlines(), '\n')
                    print(' ### INFO: Resubmitting job ' + str(idx))
                    if not options.no_exec:
                        os.system('rm '+ListErrJobName[-1])
                        os.system('rm '+ListOutJobName[-1])
                    resubmitting = resubmitting + 1
                else:
                    continue
            else:
                continue

        cmsRun = "cmsRun " + os.getcwd() + "/" + options.cfg + " outputFile=file:"+outRootName
        cmsRun = cmsRun+" maxEvents="+str(options.maxEvents)+" randseed="+str(randseed)
        if int(options.step) == 0:
            cmsRun = cmsRun+" inputFiles="+options.grid
        if int(options.step) > 0: 
            cmsRun = cmsRun+" inputFiles=file:"+inRootName
        cmsRun = cmsRun+" >& "+outLogName

        skimjob = open (outJobName, 'w')
        skimjob.write ('#!/bin/bash\n')
        skimjob.write ('export X509_USER_PROXY=~/.t3/proxy.cert\n')
        skimjob.write ('source /cvmfs/cms.cern.ch/cmsset_default.sh\n')
        skimjob.write ('cd %s/src\n' %options.cmssw)
        skimjob.write ('cmsenv\n')
        skimjob.write ('eval `scram r -sh`\n')
        skimjob.write ('cd %s\n' %(outdir + '/jobs/' + str(idx)))
        skimjob.write (cmsRun+'\n')
        skimjob.close ()

        os.system ('chmod u+rwx ' + outJobName)
        command = ('/home/llr/cms/evernazza/t3submit -'+options.queue+' \'' + outJobName +"\'")
        print(command)
        if not options.no_exec: os.system (command)