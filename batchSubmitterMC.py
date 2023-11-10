import os, glob
from datetime import datetime
from optparse import OptionParser

# Script to submit MC production

'''
python3 batchSubmitterMC.py --step 0 --cfg gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250_0_cfg.py --cmssw /data_CMS/cms/vernazza/MCProduction/2023_11_14/CMSSW_10_6_18 \
--base /data_CMS/cms/vernazza/MCProduction/2023_11_14/OutputSamples/gg_X_ZZbbtautau_quark-mass-effects_NNPDF31_13TeV_M250 \
--maxEvents 10000 --nJobs 20 --start_from 0 --queue short --no_exec
'''

if __name__ == "__main__" :

    parser = OptionParser()    
    parser.add_option("--step",      dest="step",      type=str,            default="0",                             help="Step number")
    parser.add_option("--cfg",       dest="cfg",       type=str,            default="Step_0_cfg.py",                 help="Config file")
    parser.add_option("--cmssw",     dest="cmssw",     type=str,            default="./CMSSW_10_6_18",               help="Path to CMSSW release")
    parser.add_option("--base",      dest="base",      type=str,            default=None,                            help="Base output folder name")
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

    resubmitting = 0

    starting_index = int(options.start_from)
    ending_index = starting_index + int(options.nJobs)
    print(" ### INFO: Index range", starting_index, ending_index)
    for idx in range(starting_index, ending_index):

        os.system('mkdir -p '+outdir+'/jobs')
        outJobName  = outdir + '/jobs/job_' + str(idx) + '.sh'
        outLogName  = outdir + '/jobs/log_' + str(idx) + '.txt'
        outRootName = outdir + '/Ntuple_' + str(idx) + '.root'

        # random seed for MC production should every time we submit a new generation
        # it's obtained by summing current Y+M+D+H+M+S+job_number
        # now = datetime.now()
        # randseed = int(now.year) + int(now.month) + int(now.day) + int(now.hour) + int(now.minute) + int(now.second) + idx
        randseed = idx+1 # to be reproducible

        if options.resubmit:
            ListErrJobName = glob.glob(outdir + '/jobs/job_' + str(idx) + '.sh.e*')
            ListOutJobName = glob.glob(outdir + '/jobs/job_' + str(idx) + '.sh.o*')
            if len(ListErrJobName) > 0:
                if len(os.popen('grep "No such file or directory" '+ListErrJobName[-1]).read()) > 0:
                    print('resubmitting')
                    if not options.no_exec:
                        os.system('rm '+ListErrJobName[-1])
                        os.system('rm '+ListOutJobName[-1])
                    resubmitting = resubmitting + 1
                else:
                    continue
            else:
                continue

        cmsRun = "cmsRun " + options.cfg + " outputFile=file:"+outRootName
        cmsRun = cmsRun+" maxEvents="+str(options.maxEvents)+" randseed="+str(randseed)
        cmsRun = cmsRun+" >& "+outLogName

        print(cmsRun)

        skimjob = open (outJobName, 'w')
        skimjob.write ('#!/bin/bash\n')
        skimjob.write ('export X509_USER_PROXY=~/.t3/proxy.cert\n')
        skimjob.write ('source /cvmfs/cms.cern.ch/cmsset_default.sh\n')
        skimjob.write ('cd %s\n' %options.cmssw)
        skimjob.write ('cmsenv\n')
        skimjob.write ('eval `scram r -sh`\n')
        skimjob.write ('cd %s\n' %os.getcwd())
        skimjob.write (cmsRun+'\n')
        skimjob.close ()

        os.system ('chmod u+rwx ' + outJobName)
        command = ('/home/llr/cms/evernazza/t3submit -'+options.queue+' \'' + outJobName +"\'")
        print(command)
        if not options.no_exec: os.system (command)