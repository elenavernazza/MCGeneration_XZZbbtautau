# Generating Zprime->ZH->bbtautau samples
## Madgraph cards
The original Madgraph cards are at [in the genproductions repo](https://github.com/cms-sw/genproductions/tree/7d0b3289f259c976d6a591b5dc40c60ca39460af/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/exo_diboson/Spin-1/Zprime_Zh_Zhadhbb), taken from Zprime_Zh_Zhadhbb. Z decay channel was changed from hadronic to tautau.

### instructions for creating the cards the first time
Clone the genproductions CMS repository (not in a CMSSW release area).
In a working directory, to prepare the cards :
The cards we want are in `genproductions/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/exo_diboson/Spin-1`. 
Copy the folder holding the one you want, for example : `cp -r cards/production/2017/13TeV/exo_diboson/Spin-1/Zprime_Zh_Zhadhbb ./Zprime_Zh_Ztautauhbb`
Edit the `*_proc_card.dat` file (e.g. `prime_Zh_Zbbhtautau/Zprime_Zh_Zbbhtautau_narrow_M/Zprime_Zh_Zbbhtautau_narrow_M_proc_card.dat`) and update the process *and the output name*.
Then run the `.sh` script in the folder (e.g. `chmod +x ./Zprime_Zh_Zbbhtautau/Zprime_Zh_Zbbhtautau_narrow.sh; ./Zprime_Zh_Zbbhtautau/Zprime_Zh_Zbbhtautau_narrow.sh` ) to egenrate the cards for the different mass points (edit the script to choose them).

### instructions for using already made cards
They are in bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/DY_ZprimeToZH_ZbbHtautau


## Making the gridpacks
Copy the folders with the cards into `genproductions/bin/MadGraph5_aMCatNLO`
Then run `./gridpack_generation.sh <NameOfOutputInProcCard> <pathToCardFolder>`

<details>

Steps that I ran (you need to ensure that the folder holding the cards is the same as the name of output in the card) before inclusion in official genproductions
~~~bash
cd ~/bbtautau/ZHbbtautau/gridpack-prod/genproductions/bin/MadGraph5_aMCatNLO

cp -r /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/GridpackConfiguration/Zprime_Zh_Zbbhtautau/Zprime_Zh_Zbbhtautau_narrow_M* .
rm -r Zprime_Zh_Zbbhtautau_narrow_M
for card_folder in $(ls -d Zprime_Zh_Zbbhtautau*/); do
# the & runs in background, don't close the shell before everything is done
# ${x::-1} drops the / at the end of the directory
./gridpack_generation.sh ${card_folder::-1} $card_folder
done

cp -r /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/GridpackConfiguration/Zprime_Zh_Ztautauhbb/Zprime_Zh_Ztautauhbb_narrow_M* .
rm -r Zprime_Zh_Ztautauhbb_narrow_M
for card_folder in $(ls -d Zprime_Zh_Ztautauhbb*/); do
./gridpack_generation.sh ${card_folder::-1} $card_folder
done
~~~

TO cleanup : `rm -r Zprime_Zh_Zbbhtautau_narrow_M*/Zprime_*_gridpack`

</details>

~~~bash


cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpack-prod/genproductions/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/DY_ZprimeToZH_ZbbHtautau
python3 MakeCards.py

cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpack-prod/genproductions/bin/MadGraph5_aMCatNLO
NPROCESSES=5
(
for card_folder in $(cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpack-prod/genproductions/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/DY_ZprimeToZH_ZbbHtautau; ls -d Zprime_Zh_Zbbhtautau_narrow_M*/); do
  ((i=i%NPROCESSES)); ((i++==0)) && wait # this is to ensure only NPROCESSES gridpack generations run at the same time
  # ${x::-1} drops the / at the end of the directory
  ./gridpack_generation.sh ${card_folder::-1} /cards/production/2017/13TeV/DY_ZprimeToZH_ZbbHtautau/$card_folder &
done
)

########## ZttHbb

cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpack-prod/genproductions/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/DY_ZprimeToZH_ZtautauHbb
python3 MakeCards.py

cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpack-prod/genproductions/bin/MadGraph5_aMCatNLO
NPROCESSES=5
(
for card_folder in $(cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpack-prod/genproductions/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/DY_ZprimeToZH_ZtautauHbb; ls -d Zprime_Zh_Ztautauhbb_narrow_M*/); do
  ((i=i%NPROCESSES)); ((i++==0)) && wait # this is to ensure only NPROCESSES gridpack generations run at the same time
  # ${x::-1} drops the / at the end of the directory
  ./gridpack_generation.sh ${card_folder::-1} /cards/production/2017/13TeV/DY_ZprimeToZH_ZtautauHbb/$card_folder &
done
)


## Moving the gridpacks to final location
mv /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpack-prod/genproductions/bin/MadGraph5_aMCatNLO/Zprime_Zh_Z*_narrow_M*_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks
~~~


### Drawing Feynman diagrams
~~~bash
cd genproductions/bin/MadGraph5_aMCatNLO/Zprime_Zh_Ztautauhbb_narrow_M600/Zprime_Zh_Ztautauhbb_narrow_M600_gridpack/work
./MG5_aMC_v2_9_13/bin/mg5_aMC
# inside madgraph shell, copy paste proc_card.dat
display diagrams ./

~~~

## Preparing the CMSSW config files
We are using the flow [B2G-chain_RunIIFall18wmLHEGS_flowRunIIAutumn18DRPremix_flowRunIIAutumn18MiniAOD_flowRunIIAutumn18NanoAODv7-0200](https://cms-pdmv-prod.web.cern.ch/mcm/chained_requests?prepid=B2G-chain_RunIIFall18wmLHEGS_flowRunIIAutumn18DRPremix_flowRunIIAutumn18MiniAOD_flowRunIIAutumn18NanoAODv7-02000&page=0&shown=15)

CMSSW releases are in `/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases`

<details>
<summary>v1 production of ZbbHtautau</summary>
Getting the fragment for v1: 
~~~bash
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_2_13_patch1/src
cmsenv
curl -s -k https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_fragment/B2G-RunIIFall18wmLHEGS-01094 --retry 3 --create-dirs -o Configuration/GenProduction/python/B2G-RunIIFall18wmLHEGS-01094-fragment.py
scram b
~~~

Getting the fragment for v2: 
~~~bash
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_6_19_patch3/src
cmsenv
curl -s -k https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_fragment/B2G-RunIIFall18wmLHEGS-01094 --retry 3 --create-dirs -o Configuration/GenProduction/python/B2G-RunIIFall18wmLHEGS-01094-fragment.py
# I replaced line 4 to  args = cms.vstring('ADD_CORRECT_GRIDPACK'), just in case (to make sure we don't use the B2G gridpacks, normally this is changed later in batch_submitter)
scram b
~~~
</details>

Installing the fragment for v3
~~~bash
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_6_19_patch3/src
mkdir -p Configuration/GenProduction/python
cp /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/Zprime_ZH_fragment_template.py Configuration/GenProduction/python/
# I replaced line 4 to  args = cms.vstring('ADD_CORRECT_GRIDPACK'), just in case (to make sure we don't use the B2G gridpacks, normally this is changed later in batch_submitter)
# I also removed the POWHEG-related config line (not sure about this)

cmsenv

scram b
~~~


### cmsDriver commands
`cd /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration`

The following commands were copied from the B2G production, however the nanoAOD version is old (v7) and is weird so it was not used.

<details>
<summary>Old B2G-copied process</summary>
After each step we edit the configuration file to add the OptionParser

#### Step 0 (LHE,GEN,SIM)
[LHEGS](https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=B2G-RunIIFall18wmLHEGS-01094&page=0&shown=4398046775347) 	CMSSW_10_2_13_patch1 
Raw cmsDriver command : `cmsDriver.py Configuration/GenProduction/python/B2G-RunIIFall18wmLHEGS-01094-fragment.py --python_filename B2G-RunIIFall18wmLHEGS-01094_1_cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM,LHE --fileout file:B2G-RunIIFall18wmLHEGS-01094.root --conditions 102X_upgrade2018_realistic_v11 --beamspot Realistic25ns13TeVEarly2018Collision --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="int(${SEED})" --step LHE,GEN,SIM --geometry DB:Extended --era Run2_2018 --no_exec --mc -n 50`

My commands :
~~~bash
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_2_13_patch1
cmsenv
cd /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration
cmsDriver.py Configuration/GenProduction/python/B2G-RunIIFall18wmLHEGS-01094-fragment.py --python_filename gg_Zprime_ZHtautaubb_0_cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM,LHE --fileout file:B2G-RunIIFall18wmLHEGS-01094.root --conditions 102X_upgrade2018_realistic_v11 --beamspot Realistic25ns13TeVEarly2018Collision --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=0 --step LHE,GEN,SIM --geometry DB:Extended --era Run2_2018 --no_exec --mc -n 50
~~~

You need to change the line `process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=0` at the very end of the file

#### Step 1 (DIGI,DATAMIX,L1,DIGI2RAW,HLT)
[ B2G-RunIIAutumn18DRPremix-01091 ](https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=B2G-RunIIAutumn18DRPremix-01091&page=0&shown=4398046775347) 	CMSSW_10_2_5

Raw cmsDriver commands : `cmsDriver.py  --python_filename B2G-RunIIAutumn18DRPremix-01091_1_cfg.py --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:B2G-RunIIAutumn18DRPremix-01091_0.root --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer17PrePremix-PUAutumn18_102X_upgrade2018_realistic_v15-v1/GEN-SIM-DIGI-RAW" --conditions 102X_upgrade2018_realistic_v15 --step DIGI,DATAMIX,L1,DIGI2RAW,HLT:@relval2018 --procModifiers premix_stage2 --geometry DB:Extended --filein file:B2G-RunIIFall18wmLHEGS-01094.root --datamix PreMix --era Run2_2018 --no_exec --mc -n $EVENTS`

NB : following commands takes a long time (normal) and needs grid proxy
~~~bash
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_2_5
cmsenv
cd /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration
cmsDriver.py  --python_filename gg_Zprime_ZHtautaubb_1_cfg.py --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:B2G-RunIIAutumn18DRPremix-01091_0.root --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer17PrePremix-PUAutumn18_102X_upgrade2018_realistic_v15-v1/GEN-SIM-DIGI-RAW" --conditions 102X_upgrade2018_realistic_v15 --step DIGI,DATAMIX,L1,DIGI2RAW,HLT:@relval2018 --procModifiers premix_stage2 --geometry DB:Extended --filein file:B2G-RunIIFall18wmLHEGS-01094.root --datamix PreMix --era Run2_2018 --no_exec --mc -n 50
~~~


#### Step 2 (RAW2DIGI,L1Reco,RECO,RECOSIM,EI)
[ B2G-RunIIAutumn18DRPremix-01091 second part ](https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=B2G-RunIIAutumn18DRPremix-01091&page=0&shown=4398046775347) 	CMSSW_10_2_5

Raw cmsDriver commands : `cmsDriver.py  --python_filename B2G-RunIIAutumn18DRPremix-01091_2_cfg.py --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:B2G-RunIIAutumn18DRPremix-01091.root --conditions 102X_upgrade2018_realistic_v15 --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI --procModifiers premix_stage2 --filein file:B2G-RunIIAutumn18DRPremix-01091_0.root --era Run2_2018 --runUnscheduled --no_exec --mc -n $EVENTS`

~~~bash
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_2_5
cmsenv
cd /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration
cmsDriver.py  --python_filename gg_Zprime_ZHtautaubb_2_cfg.py --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:B2G-RunIIAutumn18DRPremix-01091.root --conditions 102X_upgrade2018_realistic_v15 --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI --procModifiers premix_stage2 --filein file:B2G-RunIIAutumn18DRPremix-01091_0.root --era Run2_2018 --runUnscheduled --no_exec --mc -n 50
~~~

#### Step3 (MINIAODSIM)
[ B2G-RunIIAutumn18MiniAOD-01089 ](https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=B2G-RunIIAutumn18MiniAOD-01089&page=0&shown=4398046775347) 	CMSSW_10_2_5


Raw cmsDriver commands : `cmsDriver.py  --python_filename B2G-RunIIAutumn18MiniAOD-01089_1_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:B2G-RunIIAutumn18MiniAOD-01089.root --conditions 102X_upgrade2018_realistic_v15 --step PAT --geometry DB:Extended --filein "dbs:/ZprimeToZhToZhadhbb_narrow_M-1000_13TeV-madgraph/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM" --era Run2_2018 --runUnscheduled --no_exec --mc -n $EVENTS`

~~~bash
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_2_5
cmsenv
cd /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration
cmsDriver.py  --python_filename gg_Zprime_ZHtautaubb_3_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:B2G-RunIIAutumn18MiniAOD-01089.root --conditions 102X_upgrade2018_realistic_v15 --step PAT --geometry DB:Extended --filein "dbs:/ZprimeToZhToZhadhbb_narrow_M-1000_13TeV-madgraph/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM" --era Run2_2018 --runUnscheduled --no_exec --mc -n 50
~~~


#### Step4 (NANOAODSIM)
[ B2G-RunIIAutumn18NanoAODv7-02003 ](https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=B2G-RunIIAutumn18NanoAODv7-02003&page=0&shown=4398046775347) 		
CMSSW_10_2_22


Raw cmsDriver commands : `cmsDriver.py  --python_filename B2G-RunIIAutumn18NanoAODv7-02003_1_cfg.py --eventcontent NANOEDMAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:B2G-RunIIAutumn18NanoAODv7-02003.root --conditions 102X_upgrade2018_realistic_v21 --step NANO --filein "dbs:/ZprimeToZhToZhadhbb_narrow_M-1000_13TeV-madgraph/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM" --era Run2_2018,run2_nanoAOD_102Xv1 --no_exec --mc -n $EVENTS`

~~~bash
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/cmsReleases/CMSSW_10_2_22
cmsenv
cd /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration
cmsDriver.py  --python_filename gg_Zprime_ZHtautaubb_4_cfg.py --eventcontent NANOEDMAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:B2G-RunIIAutumn18NanoAODv7-02003.root --conditions 102X_upgrade2018_realistic_v21 --step NANO --filein "dbs:/ZprimeToZhToZhadhbb_narrow_M-1000_13TeV-madgraph/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM" --era Run2_2018,run2_nanoAOD_102Xv1 --no_exec --mc -n 50
~~~

</details>


We copied the commands from a Drell-Yan production found on cmsdas
#### Commands used for DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8 (2018 UL)
 - [LHEGEN](https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=EGM-RunIISummer20UL18wmLHEGEN-00001&shown=4458623), CMSSW_10_6_19_patch3 : `cmsDriver.py Configuration/GenProduction/python/EGM-RunIISummer20UL18wmLHEGEN-00001-fragment.py --python_filename EGM-RunIISummer20UL18wmLHEGEN-00001_1_cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN,LHE --fileout file:EGM-RunIISummer20UL18wmLHEGEN-00001.root --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --customise_commands process.source.numberEventsInLuminosityBlock="cms.untracked.uint32(270)" --step LHE,GEN --geometry DB:Extended --era Run2_2018 --no_exec --mc -n $EVENTS`
 - [sim](https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=EGM-RunIISummer20UL18SIM-00002&page=0&shown=2151678079) 	
CMSSW_10_6_17_patch1 : `cmsDriver.py  --python_filename EGM-RunIISummer20UL18SIM-00002_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --fileout file:EGM-RunIISummer20UL18SIM-00002.root --conditions 106X_upgrade2018_realistic_v11_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision --step SIM --geometry DB:Extended --filein file:EGM-RunIISummer20UL18wmLHEGEN-00001.root --era Run2_2018 --runUnscheduled --no_exec --mc -n $EVENTS `
 - [DigiPremix](https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=EGM-RunIISummer20UL18DIGIPremix-00002&page=0&shown=127) CMSSW_10_6_17_patch1 : ` cmsDriver.py  --python_filename EGM-RunIISummer20UL18DIGIPremix-00002_1_cfg.py --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-DIGI --fileout file:EGM-RunIISummer20UL18DIGIPremix-00002.root --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX" --conditions 106X_upgrade2018_realistic_v11_L1v1 --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 --geometry DB:Extended --filein file:EGM-RunIISummer20UL18SIM-00002.root --datamix PreMix --era Run2_2018 --runUnscheduled --no_exec --mc -n $EVENTS `
  - [HLT](https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=EGM-RunIISummer20UL18HLT-00002&page=0&shown=127) 	
CMSSW_10_2_16_UL : `cmsDriver.py  --python_filename EGM-RunIISummer20UL18HLT-00002_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:EGM-RunIISummer20UL18HLT-00002.root --conditions 102X_upgrade2018_realistic_v15 --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' --step HLT:2018v32 --geometry DB:Extended --filein file:EGM-RunIISummer20UL18DIGIPremix-00002.root --era Run2_2018 --no_exec --mc -n $EVENTS`
 - [RECO](https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=EGM-RunIISummer20UL18RECO-00002&page=0&shown=2151678079), 	
CMSSW_10_6_17_patch1 : `cmsDriver.py  --python_filename EGM-RunIISummer20UL18RECO-00002_1_cfg.py --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:EGM-RunIISummer20UL18RECO-00002.root --conditions 106X_upgrade2018_realistic_v11_L1v1 --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI --geometry DB:Extended --filein file:EGM-RunIISummer20UL18HLT-00002.root --era Run2_2018 --runUnscheduled --no_exec --mc -n $EVENTS`
 - [MINI](https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=EGM-RunIISummer20UL18MiniAODv2-00004&page=0&shown=4194431) CMSSW_10_6_20 : `cmsDriver.py  --python_filename EGM-RunIISummer20UL18MiniAODv2-00004_1_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:EGM-RunIISummer20UL18MiniAODv2-00004.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step PAT --procModifiers run2_miniAOD_UL --geometry DB:Extended --filein "dbs:/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v1/AODSIM" --era Run2_2018 --runUnscheduled --no_exec --mc -n $EVENTS `
 - [NANO](https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=EGM-RunIISummer20UL18NanoAODv9-00005&page=0&shown=127) 
CMSSW_10_6_26 : `cmsDriver.py  --python_filename EGM-RunIISummer20UL18NanoAODv9-00005_1_cfg.py --eventcontent NANOEDMAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:EGM-RunIISummer20UL18NanoAODv9-00005.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --customise_commands "process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False))) \\n from PhysicsTools.NanoAOD.custom_jme_cff import PrepJMECustomNanoAOD_MC; PrepJMECustomNanoAOD_MC(process)" --step NANO --filein "dbs:/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM" --era Run2_2018,run2_nanoAOD_106Xv2 --no_exec --mc -n $EVENTS`

## Running the jobs
### Snippets
~~~bash
# if you just want to check proxy validity
export X509_USER_PROXY=~/.t3/proxy.cert
voms-proxy-info
# check fot timeleft: xx:xx:xx
~~~

### Testing locally (version 1 pilot)

~~~bash
source /opt/exp_soft/cms/t3/t3setup

mkdir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobsPilots
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobsPilots

SCRIPT=/home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/batchSubmitterMC_all.py
BASE_DIR=/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobsPilots

~~~

#### Zh_Zbbhtautau
##### Using B2G-copied config
~~~bash
cd $BASE_DIR
MASS=600
mkdir gg_Zh_Zbbhtautau_M$MASS
cd gg_Zh_Zbbhtautau_M$MASS
cp /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/gg_Zprime_ZHtautaubb_*_cfg.py .

python3 $SCRIPT \
--process gg_Zprime_ZHtautaubb \
--grid /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/pilot/Zprime_Zh_Zbbhtautau_narrow_M$MASS\_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 100 --nJobs 1 --start_from 0 --queue long \
--base $(pwd) \
--no_exec
~~~

##### Using ZZ config
~~~bash
cd $BASE_DIR
MASS=600
mkdir gg_Zh_Zbbhtautau_M$MASS
cd gg_Zh_Zbbhtautau_M$MASS
cp /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/gg_X_ZZbbtautau*_cfg.py .

python3 $SCRIPT \
--process gg_X_ZZbbtautau \
--grid /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/pilot/Zprime_Zh_Zbbhtautau_narrow_M$MASS\_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 100 --nJobs 1 --start_from 0 --queue long \
--base $(pwd) \
--no_exec
~~~

#### Zh_Ztautauhbb
For now we use the same config files as ZZ, just changing the gridpack
~~~bash
cd $BASE_DIR
MASS=600
mkdir gg_Zh_Ztautauhbb_M$MASS
cd gg_Zh_Ztautauhbb_M$MASS
cp /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/gg_X_ZZbbtautau_*_cfg.py .

# same process as Zh_Zbbhtautau for now, but different gridpacj
python3 $SCRIPT \
--process gg_X_ZZbbtautau \
--grid /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/pilot/Zprime_Zh_Ztautauhbb_narrow_M$MASS\_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 100 --nJobs 1 --start_from 0 --queue long \
--base $(pwd) \
--no_exec
~~~

### Runs version 1
~~~bash
source /opt/exp_soft/cms/t3/t3setup

mkdir /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs

SCRIPT=/home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/batchSubmitterMC_all.py
BASE_DIR=/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs

~~~

#### Pilot ZHtautaubb first version
~~~bash
cd $BASE_DIR
MASS=600
mkdir gg_X_ZZbbtautau_M$MASS
cd gg_X_ZZbbtautau_M$MASS
cp /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/gg_Zprime_ZHtautaubb_*_cfg.py .

python3 $SCRIPT \
--process gg_Zprime_ZHtautaubb \
--grid /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/pilot/Zprime_Zh_Zbbhtautau_narrow_M$MASS\_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 1000 --nJobs 50 --start_from 0 --queue long \
--base $(pwd) \
--no_exec
~~~

#### Zh_Zbbhtautau (using ZZ config)
~~~bash
cd $BASE_DIR
MASS=600
mkdir Zprime_Zh_Zbbhtautau_M$MASS
cd Zprime_Zh_Zbbhtautau_M$MASS
cp /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/gg_X_ZZbbtautau*_cfg.py .

python3 $SCRIPT \
--process gg_X_ZZbbtautau \
--grid /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/GridpacksZH/Zprime_Zh_Zbbhtautau_narrow_M$MASS\_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 100 --nJobs 50 --start_from 0 --queue long \
--base $(pwd) \
--no_exec
~~~

#### Zh_Ztautauhbb (using ZZ config)
~~~bash
cd $BASE_DIR
MASS=600
mkdir Zprime_Zh_Ztautauhbb_M$MASS
cd Zprime_Zh_Ztautauhbb_M$MASS
cp /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/gg_X_ZZbbtautau*_cfg.py .

python3 $SCRIPT \
--process gg_X_ZZbbtautau \
--grid /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/GridpacksZH/Zprime_Zh_Ztautauhbb_narrow_M$MASS\_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 100 --nJobs 50 --start_from 0 --queue long \
--base $(pwd) \
--no_exec
~~~

### Runs version 2
~~~bash
cd $BASE_DIR
MASS=600
mkdir Zprime_Zh_Zbbhtautau_M$MASS
cd Zprime_Zh_Zbbhtautau_M$MASS

python3 $SCRIPT \
--process Zprime_Zh_Zbbhtautau_v2 \
--grid /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/GridpacksZH/Zprime_Zh_Zbbhtautau_narrow_M$MASS\_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 1000 --nJobs 50 --start_from 0 --queue long \
--base $(pwd) \
--no_exec
~~~

### Runs version 3
With new gridpacks (same as those used for central production), with cut_decays = true

~~~bash
SCRIPT=/home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/batchSubmitterMC_all.py
BASE_DIR=/grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/jobs/Zprime_v3

for MASS in 3000 4000; do
cd $BASE_DIR
mkdir Zprime_Zh_Zbbhtautau_M$MASS
cd Zprime_Zh_Zbbhtautau_M$MASS

python3 $SCRIPT \
--process Zprime_Zh_Zbbhtautau_v2 \
--grid /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/Zprime_Zh_Zbbhtautau_narrow_M$MASS\_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 1000 --nJobs 200 --start_from 0 --queue long \
--base $(pwd) 
done

## ZttHbb
for MASS in 3000 4000; do
cd $BASE_DIR
mkdir Zprime_Zh_Ztautauhbb_M$MASS
cd Zprime_Zh_Ztautauhbb_M$MASS

python3 $SCRIPT \
--process Zprime_Zh_Zbbhtautau_v2 \
--grid /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpacks/Zprime_Zh_Ztautauhbb_narrow_M$MASS\_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz \
--maxEvents 1000 --nJobs 200 --start_from 0 --queue long \
--base $(pwd) 
done
~~~


# Generating gg->A->ZH->bbtautau samples
Cards are taken from `GluGluToAToZhToLLBB M-225 13TeV-madgraphMLM-pythia8` (HIG-18-005, [cards](https://github.com/cms-sw/genproductions/blob/master/bin/MadGraph5_aMCatNLO/cards/production/13TeV/HToZATo2L2B_gg-fusion_b-associatedproduction/run2Template_cards/template_HToZATo2L2B_500p00_300p00_1p50_ggH_TuneCP5_13TeV_pythia8/HToZATo2L2B_500p00_300p00_1p50_ggH_TuneCP5_13TeV_pythia8_run_card.dat)) and `GluGluToAToZhToLLTauTau M* TuneCP5 13TeV-madgraphMLM-pythia8` (HIG-22-011, [cards](https://github.com/cms-sw/genproductions/tree/c2d6dbe65cbefb523cf3f7beb71cb452ff107235/bin/MadGraph5_aMCatNLO/cards/production/13TeV/AToZhToLLTT_01j_4f)).

## Model
The madgraph model used is [2HDMtII_NLO](https://feynrules.irmp.ucl.ac.be/wiki/2HDM), "UFO model with QCD corrections for the type II 2HDM, both the top and bottom are massive and their yukawa are renormalized like their masses, i.e. on-shell."

PDGids (see particles.py in model, spin is in 2S+1 notation):
 - a - 22 - photon
 - h1 - 25 - light higgs h_0
 - h2 - 35 - heavy Higgs H_0
 - h3 - 36 - pseudoscalar higgs A_0
 - H+ - 37 - charged higgs

A_0 decays (see decays.py in model):
 - a h1, a h2, h2 z
 - b bar
 - t tbar
 - tau tau
 - h1 z (ZH)
 - h+ W-, h- W+

## Original cards
### A->Zh->lltautau
~~~
define ell+ = e+ mu+ ta+
define ell- = e- mu- ta-

generate g g > h3 [QCD] @0
add process p p > h3 j [QCD] @1

# madspin_card
set spinmode none
decay h3 > h1 z, h1 > ta+ ta-, z > ell+ ell-

# run_card
#*********************************************************************
# Matching - Warning! ickkw > 1 is still beta
#*********************************************************************
 1        = ickkw            ! 0 no matching, 1 MLM, 2 CKKW matching
 1        = highestmult      ! for ickkw=2, highest mult group
 1        = ktscheme         ! for ickkw=1, 1 Durham kT, 2 Pythia pTE
 1        = alpsfact         ! scale factor for QCD emission vx
 F        = chcluster        ! cluster only according to channel diag
 F        = pdfwgt           ! for ickkw=1, perform pdf reweighting
 4        = asrwgtflavor     ! highest quark flavor for a_s reweight
 T        = clusinfo         ! include clustering tag in output
 3.0      = lhe_version       ! Change the way clustering information pass to shower.   
~~~

### A->ZH->llbb
I could not find the cards on genproductions (only the script generating them and the template cards for H->ZA), so I extracted them from the gridpacks at `/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/AToZHTo2L2B_200p00_125p00_1p50_ggH_TuneCP5_13TeV_pythia8/v1/AToZHTo2L2B_200p00_125p00_1p50_ggH_TuneCP5_13TeV_pythia8_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz`

~~~
import model 2HDMtII_NLO
#gg fusion -loop induced
generate p p > h3 > h2 l+ l- $$ a [QCD] @0

# madspin
set spinmode none               # Use one of the madspin special mode
set max_weight_ps_point 400     # number of PS to estimate the maximum for each event
# specify the decay for the final state particles
decay h2 > b b~

#run_card extract
#*********************************************************************
## Matching - Warning! ickkw > 1 is still beta
##*********************************************************************
  0	= ickkw ! 0 no matching, 1 MLM
  1.0	= alpsfact ! scale factor for QCD emission vx
  False	= chcluster ! cluster only according to channel diag
  5	= asrwgtflavor ! highest quark flavor for a_s reweight
  False	= auto_ptj_mjj ! Automatic setting of ptj and mjj if xqcut >0
                       ! (turn off for VBF and single top processes)
  0.	= xqcut            ! minimum kt jet measure between partons
  1     = highestmult      ! for ickkw=2, highest mult group
  1     = ktscheme         ! for ickkw=1, 1 Durham kT, 2 Pythia pTE
  False = chcluster        ! cluster only according to channel diag
  False = pdfwgt           ! for ickkw=1, perform pdf reweighting
  True  = clusinfo         ! include clustering tag in output
  3.0   = lhe_version      ! Change the way clustering information pass to shower.  
~~~

## Making cards
### decisions
 - matching : took AToZHTo2L2B settings (no matching)
 - bwcutoff : took AToZHTo2L2B = default = 15 (AToZhToLLTT_01j_4f uses 15000 for some reason ?)


## Making the gridpacks
Copy the folders with the cards into `genproductions/bin/MadGraph5_aMCatNLO`
Then run `./gridpack_generation.sh <NameOfOutputInProcCard> <pathToCardFolder>`


Steps that I ran (you need to ensure that the folder holding the cards is the same as the name of output in the card)
~~~bash
cd /grid_mnt/data__data.polcms/cms/cuisset/ZHbbtautau/gridpack-prod/genproductions/bin/MadGraph5_aMCatNLO

cp -r /home/llr/cms/cuisset/bbtautau/ZHbbtautau/MCGeneration/GridpackConfiguration/gg_A_Zh_Zbbhtautau/gg_A_Zh_Zbbhtautau_M* .

for card_folder in $(ls -d Zprime_Zh_Zbbhtautau*/); do
# the & runs in background, don't close the shell before everything is done
# ${x::-1} drops the / at the end of the directory
./gridpack_generation.sh ${card_folder::-1} $card_folder
done
~~~

### Drawing Feynman diagrams
~~~bash
cd gg_A_Zh_Zbbhtautau_M600/gg_A_Zh_Zbbhtautau_M600_gridpack/work/
./MG5_aMC_v2_9_13/bin/mg5_aMC
# inside madgraph shell, copy paste proc_card.dat
display diagrams ./

~~~
