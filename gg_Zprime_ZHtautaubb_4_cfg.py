# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: --python_filename gg_Zprime_ZHtautaubb_4_cfg.py --eventcontent NANOEDMAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:B2G-RunIIAutumn18NanoAODv7-02003.root --conditions 102X_upgrade2018_realistic_v21 --step NANO --filein dbs:/ZprimeToZhToZhadhbb_narrow_M-1000_13TeV-madgraph/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM --era Run2_2018,run2_nanoAOD_102Xv1 --no_exec --mc -n 50
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

from Configuration.StandardSequences.Eras import eras

options = VarParsing.VarParsing ('analysis')
options.inputFiles = ''
options.outputFile = ''
options.maxEvents = -1
options.register ('randseed',
                  "", # default value
                  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.VarParsing.varType.string,         # string, int, or float
                  "which seed to use?")
options.parseArguments()

process = cms.Process('NANO',eras.Run2_2018,eras.run2_nanoAOD_102Xv1)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.NanoAOD.nano_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

# change the seed for each submission
process.RandomNumberGeneratorService.generator.initialSeed = int(options.randseed)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)

# Input source
process.source = cms.Source("PoolSource",
    # fileNames = cms.untracked.vstring(
    #     '/store/mc/RunIIAutumn18MiniAOD/ZprimeToZhToZhadhbb_narrow_M-1000_13TeV-madgraph/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/270000/063C6EA9-3807-C844-8E23-F7E32681030E.root', 
    #     '/store/mc/RunIIAutumn18MiniAOD/ZprimeToZhToZhadhbb_narrow_M-1000_13TeV-madgraph/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/270000/1581FB3B-57AF-7340-9209-9131CB0A75F0.root', 
    #     '/store/mc/RunIIAutumn18MiniAOD/ZprimeToZhToZhadhbb_narrow_M-1000_13TeV-madgraph/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/270000/72C43B9F-6ED2-DE49-B0BB-306446F2F6F6.root', 
    #     '/store/mc/RunIIAutumn18MiniAOD/ZprimeToZhToZhadhbb_narrow_M-1000_13TeV-madgraph/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/270000/4FDB0F92-F88F-0747-929D-39172C8F01B4.root', 
    #     '/store/mc/RunIIAutumn18MiniAOD/ZprimeToZhToZhadhbb_narrow_M-1000_13TeV-madgraph/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/270000/4F8EBFDF-2903-9046-9B40-7CADB04BF2C4.root', 
    #     '/store/mc/RunIIAutumn18MiniAOD/ZprimeToZhToZhadhbb_narrow_M-1000_13TeV-madgraph/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/270000/C989B450-87F9-8046-81B0-F36F7D4A4F72.root'
    # ),
    fileNames = cms.untracked.vstring(options.inputFiles),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step4 nevts:'+str(options.maxEvents)),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.NANOEDMAODSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAODSIM'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string(options.outputFile),
    outputCommands = process.NANOAODSIMEventContent.outputCommands
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '102X_upgrade2018_realistic_v21', '')

# Path and EndPath definitions
process.nanoAOD_step = cms.Path(process.nanoSequenceMC)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOEDMAODSIMoutput_step = cms.EndPath(process.NANOEDMAODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.nanoAOD_step,process.endjob_step,process.NANOEDMAODSIMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_cff
from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeMC 

#call to customisation function nanoAOD_customizeMC imported from PhysicsTools.NanoAOD.nano_cff
process = nanoAOD_customizeMC(process)

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
