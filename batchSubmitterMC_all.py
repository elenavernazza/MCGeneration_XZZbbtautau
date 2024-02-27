import os, glob, sys
from datetime import datetime
from optparse import OptionParser

""" Config dictionnary. Key is name to be passed as command line argument. Value is array of processing steps in order.
Can sepecify either "cfg" : cmssw python config to be run using cmsRun, or "cmsDriver" : string of commands to be passed to cmsDriver.py
"""
multi_conf_dict = {
"gg_X_ZZbbtautau" : [
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
      "KeepOutput": True,
    }
],
"gg_Zprime_ZHtautaubb_v1" : [ # first version of ZtautauHbb config, uses MiniAODv1 which causes problems for nanoAOD production later on
    {
      "release": "CMSSW_10_2_13_patch1",
      "cfg": "gg_Zprime_ZHtautaubb_0_cfg.py",
      "KeepOutput": False,
    },
    {
      "release": "CMSSW_10_2_5",
      "cfg": "gg_Zprime_ZHtautaubb_1_cfg.py",
      "KeepOutput": False,
    },
    {
      "release": "CMSSW_10_2_5",
      "cfg": "gg_Zprime_ZHtautaubb_2_cfg.py",
      "KeepOutput": False,
    },
    {
      "release": "CMSSW_10_2_5",
      "cfg": "gg_Zprime_ZHtautaubb_3_cfg.py",
      "KeepOutput": True,
    },
    {
      "release": "CMSSW_10_2_22",
      "cfg": "gg_Zprime_ZHtautaubb_4_cfg.py",
      "KeepOutput": True,
    },
],
"Zprime_Zh_Zbbhtautau_v2" : [ # second version of Zprime_Zh_Zbbhtautau, based on MiniAODv2 and nanoAODv9 (copied from DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8 production for RunIISummer20UL18)
    { # LHE,GEN
      "release": "CMSSW_10_6_19_patch3", 
      "cmsDriver": 'cmsDriver.py Configuration/GenProduction/python/B2G-RunIIFall18wmLHEGS-01094-fragment.py --python_filename B2G-RunIIFall18wmLHEGS-01094_1_cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN,LHE --fileout file:EGM-RunIISummer20UL18wmLHEGEN-00001.root --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --customise_commands process.source.numberEventsInLuminosityBlock="cms.untracked.uint32(270)" --step LHE,GEN --geometry DB:Extended --era Run2_2018 --mc',
      "KeepOutput": False,
    },
    { # SIM,
      "release": "CMSSW_10_6_17_patch1",
      "cmsDriver": "cmsDriver.py --python_filename EGM-RunIISummer20UL18SIM-00002_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --fileout file:EGM-RunIISummer20UL18SIM-00002.root --conditions 106X_upgrade2018_realistic_v11_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision --step SIM --geometry DB:Extended --filein file:EGM-RunIISummer20UL18wmLHEGEN-00001.root --era Run2_2018 --runUnscheduled  --mc",
      "KeepOutput": False,
    },
    { # DIGI,DATAMIX,L1,DIGI2RAW
      "release": "CMSSW_10_6_17_patch1",
      "cmsDriver": 'cmsDriver.py --python_filename EGM-RunIISummer20UL18DIGIPremix-00002_1_cfg.py --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-DIGI --fileout file:EGM-RunIISummer20UL18DIGIPremix-00002.root --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX" --conditions 106X_upgrade2018_realistic_v11_L1v1 --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 --geometry DB:Extended --filein file:EGM-RunIISummer20UL18SIM-00002.root --datamix PreMix --era Run2_2018 --runUnscheduled  --mc',
      "KeepOutput": False,
    },
    { # HLT
      "release": "CMSSW_10_2_16_UL",
      "cmsDriver": 'cmsDriver.py  --python_filename EGM-RunIISummer20UL18HLT-00002_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:EGM-RunIISummer20UL18HLT-00002.root --conditions 102X_upgrade2018_realistic_v15 --customise_commands \'process.source.bypassVersionCheck = cms.untracked.bool(True)\' --step HLT:2018v32 --geometry DB:Extended --filein file:EGM-RunIISummer20UL18DIGIPremix-00002.root --era Run2_2018 --mc',
      "KeepOutput": False,
    },
    { # RECO
      "release": "CMSSW_10_6_17_patch1",
      "cmsDriver": 'cmsDriver.py --python_filename EGM-RunIISummer20UL18RECO-00002_1_cfg.py --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:EGM-RunIISummer20UL18RECO-00002.root --conditions 106X_upgrade2018_realistic_v11_L1v1 --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI --geometry DB:Extended --filein file:EGM-RunIISummer20UL18HLT-00002.root --era Run2_2018 --runUnscheduled  --mc',
      "KeepOutput": False,
    },
    {  # MINIAOD
      "release": "CMSSW_10_6_20",
      "cmsDriver": 'cmsDriver.py --python_filename EGM-RunIISummer20UL18MiniAODv2-00004_1_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:EGM-RunIISummer20UL18MiniAODv2-00004.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step PAT --procModifiers run2_miniAOD_UL --geometry DB:Extended --filein "file:EGM-RunIISummer20UL18RECO-00002.root" --era Run2_2018 --runUnscheduled  --mc',
      "KeepOutput": True,
    },
    { # NANO
      "release": "CMSSW_10_6_27", # nanoaod twiki says CMSSW_10_6_27, DY prod used CMSSW_10_6_26 + changed NANOEDMAODSIM to NANOAODSIM
      "cmsDriver": 'cmsDriver.py --python_filename EGM-RunIISummer20UL18NanoAODv9-00005_1_cfg.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:EGM-RunIISummer20UL18NanoAODv9-00005.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --customise_commands "process.add_(cms.Service(\'InitRootHandlers\', EnableIMT = cms.untracked.bool(False))) \\n from PhysicsTools.NanoAOD.custom_jme_cff import PrepJMECustomNanoAOD_MC; PrepJMECustomNanoAOD_MC(process)" --step NANO --filein "dbs:/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM" --era Run2_2018,run2_nanoAOD_106Xv2  --mc',
      "KeepOutput": True,
    },
]
}

def findCmsswRelease(releaseName:str) -> str:
    """ Finds CMSSW release location (created with cmsrel). Returns path to src folder, ie  /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_2_22/src/ """
    bases = ["/grid_mnt/data__data.polcms/cms/vernazza/MCProduction/2023_11_14",
             "/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases"]
    for base in bases:
        pathToSrc = os.path.join(base, releaseName, "src")
        if os.path.isdir(pathToSrc):
            return pathToSrc
    raise RuntimeError("Could not find CMSSW release version " + releaseName)

# Script to submit MC production

if __name__ == "__main__" :

    parser = OptionParser()    
    parser.add_option("--base",      dest="base",      type=str,            default=None,                            help="Base output folder name")
    parser.add_option("--grid",      dest="grid",      type=str,            default=None,                            help="Gridpack location for step 0")
    parser.add_option("--process",   dest="process",   type=str,            default=None,                            help="Name of process ["+', '.join(multi_conf_dict.keys())+"]")
    parser.add_option("--maxEvents", dest="maxEvents", type=int,            default=50,                              help="Number of events per job")
    parser.add_option("--nJobs",     dest="nJobs",     type=int,            default=1,                               help="Number of jobs")
    parser.add_option("--start_from",dest="start_from",type=int,            default=0,                               help="Start random seed from")
    parser.add_option("--queue",     dest="queue",     type=str,            default='reserv',                        help="long or short queue")
    parser.add_option("--no_exec",   dest="no_exec",   action='store_true', default=False)
    parser.add_option("--resubmit",  dest="resubmit",  action='store_true', default=False)
    (options, args) = parser.parse_args()

    try:
        conf_dict = multi_conf_dict[options.process]
    except KeyError as e:
        print("Invalid process specified (" + str(e) + ")", file=sys.stderr)
        print("Possible options : " + ', '.join(multi_conf_dict.keys()))
        sys.exit(-5)
    
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
            outFileName = 'Step_' + str(step) + '_Ntuple_' + str(idx) + '.root' # filename in case of keeping the output on worker node
            outRootName = cur_dir + '/Ntuple_' + str(idx) + '.root'
            if step > 0:
                prev_dir = outdir + '/Step_' + str(step-1)
                inFileName = 'Step_' + str(step-1) +'_Ntuple_' + str(idx) + '.root' # filename in case input was kept on worker node
                inRootName = prev_dir + '/' + 'Ntuple_' + str(idx) + '.root'
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

            cfg = conf_dict[step].get('cfg', None)
            cmsDriverCommand = conf_dict[step].get('cmsDriver', None)
            assert (cfg is None) ^ (cmsDriverCommand is None), "In config, either cfg or cmsDriver must be set (not both)"
            release = conf_dict[step]['release']
            keep_previousStep = True if int(step) == 0 else conf_dict[int(step-1)]['KeepOutput']
            keep_currentStep = conf_dict[int(step)]['KeepOutput']

            scriptRun = 'cd "' + findCmsswRelease(release) + '"\n'
            scriptRun += 'cmsenv\n'
            scriptRun += 'eval `scram r -sh`\n'
            #scriptRun += 'cd %s\n' %(outdir + '/jobs/' + str(idx))
            scriptRun += 'cd -\n' # go back to job directory on node
            if cfg is not None: # cmsRun mode
              scriptRun += "cmsRun " + os.getcwd() + "/" + cfg + " outputFile=file:"+ (outRootName if keep_currentStep else outFileName) + \
                  " maxEvents="+str(options.maxEvents)+" randseed="+str(randseed)
              if step == 0: scriptRun = scriptRun+" inputFiles="+options.grid
              if int(step) > 0: 
                  scriptRun = scriptRun+" inputFiles=file:"+ (inRootName if keep_previousStep else inFileName)
              scriptRun += " >& "+outLogName + '\n'

            else: # cmsDriver mode
                scriptRun += cmsDriverCommand + f" --no_exec --python_filename Step_{step}_cfg.py -n {str(options.maxEvents)} "
                if int(step) > 0:
                  scriptRun += f"--filein 'file:{(inRootName if keep_previousStep else inFileName)}' "
                scriptRun += f"--fileout 'file:{(outRootName if keep_currentStep else outFileName)}' "
                
                scriptRun += "\n"
                scriptRun += f"echo 'process.RandomNumberGeneratorService.generator.initialSeed = {str(randseed)}' >> Step_{step}_cfg.py\n"
                if step == 0:
                  scriptRun += f"echo 'process.RandomNumberGeneratorService.externalLHEProducer.initialSeed = {str(randseed)}' >> Step_{step}_cfg.py\n"
                  scriptRun += f"echo 'process.externalLHEProducer.args = cms.vstring(\"{options.grid}\")' >> Step_{step}_cfg.py\n"
                  scriptRun += f"echo 'process.externalLHEProducer.nEvents = cms.untracked.uint32({options.maxEvents})' >> Step_{step}_cfg.py\n"
                scriptRun += f"cmsRun -n 8 Step_{step}_cfg.py  >&{outLogName}\n"

            
            if int(step) > 0 and not keep_previousStep:
                scriptRun += "rm "+inFileName + '\n'
            cmsRuns.append(scriptRun)

        if not options.resubmit:
            skimjob = open (outJobName, 'w')
            skimjob.write ('#!/bin/bash\n')
            skimjob.write ('set -e\n') # abort script at first error
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
        command = ('/opt/exp_soft/cms/t3/t3submit -8c -'+options.queue+' \'' + outJobName +"\'")
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
