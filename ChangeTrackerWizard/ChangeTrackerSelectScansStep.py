from __main__ import qt, ctk

from ChangeTrackerStep import *
from Helper import *

class ChangeTrackerSelectScansStep( ChangeTrackerStep ) :

  def __init__( self, stepid ):
    print 'Select scans: init'
    self.initialize( stepid )
    self.setName( '1. Select input scans' )
    self.setDescription( 'Select the baseline and follow-up scans to be compared.' )

    self.__parent = super( ChangeTrackerSelectScansStep, self )

  def createUserInterface( self ):
    '''
    '''
    print 'SelectScans step: createInterface'
    # TODO: might make sense to hide the button for the last step at this
    # point, but the widget does not have such option
    self.__layout = self.__parent.createUserInterface()
   
    baselineScanLabel = qt.QLabel( 'Baseline scan:' )
    self.__baselineVolumeSelector = slicer.qMRMLNodeComboBox()
    self.__baselineVolumeSelector.toolTip = "Choose the baseline scan"
    self.__baselineVolumeSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
    self.__baselineVolumeSelector.setMRMLScene(slicer.mrmlScene)
    self.__baselineVolumeSelector.addEnabled = 0

    followupScanLabel = qt.QLabel( 'Followup scan:' )
    self.__followupVolumeSelector = slicer.qMRMLNodeComboBox()
    self.__followupVolumeSelector.toolTip = "Choose the followup scan"
    self.__followupVolumeSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
    self.__followupVolumeSelector.setMRMLScene(slicer.mrmlScene)
    self.__followupVolumeSelector.addEnabled = 0
   
    loadDataButton = qt.QPushButton('Load test data')
    self.__layout.addRow(loadDataButton)
    loadDataButton.connect('clicked()', self.loadData)

    self.__layout.addRow( baselineScanLabel, self.__baselineVolumeSelector )
    self.__layout.addRow( followupScanLabel, self.__followupVolumeSelector )

    self.updateWidgetFromParameters(self.parameterNode())

  def loadData(self):
    vl = slicer.modules.volumes.logic()
    vl.AddArchetypeVolume('http://www.slicer.org/slicerWiki/images/5/59/RegLib_C01_1.nrrd', 'Meningioma1', 0)
    vl.AddArchetypeVolume('http://www.slicer.org/slicerWiki/images/e/e3/RegLib_C01_2.nrrd', 'Meningioma2', 0)

  def validate( self, desiredBranchId ):
    '''
    '''
    print 'SelectScans step: validate'
    self.__parent.validate( desiredBranchId )

    # check here that the selectors are not empty
    baseline = self.__baselineVolumeSelector.currentNode()
    followup = self.__followupVolumeSelector.currentNode()

    if baseline != None and followup != None:
      baselineID = baseline.GetID()
      followupID = followup.GetID()
      if baselineID != '' and followupID != '' and baselineID != followupID:
    
        pNode = self.parameterNode()
        pNode.SetParameter('baselineVolumeID', baselineID)
        pNode.SetParameter('followupVolumeID', followupID)
        
        lm = slicer.app.layoutManager()
        lm.setLayout(3)
        # TODO: initialize Bg/Fg, fit volumes to slice viewer
        self.__parent.validationSucceeded(desiredBranchId)
      else:
        self.__parent.validationFailed(desiredBranchId, 'Error','Please select distinctive baseline and followup volumes!')
    else:
      self.__parent.validationFailed(desiredBranchId, 'Error','Please select both baseline and followup volumes!')

  def onEntry(self, comingFrom, transitionType):
    print 'SelectScans step: onEntry'
    super(ChangeTrackerSelectScansStep, self).onEntry(comingFrom, transitionType)
    #self.updateWidgetFromParameters(self.parameterNode())
    #super(ChangeTrackerSelectScansStep, self).onEntry(comingFrom, transitionType)

  def onExit(self, goingTo, transitionType):
    print 'SelectScans step: onExit'
    super(ChangeTrackerSelectScansStep, self).onExit(goingTo, transitionType) 

  def updateWidgetFromParameters(self, parameterNode):
    baselineVolumeID = parameterNode.GetParameter('baselineVolumeID')
    followupVolumeID = parameterNode.GetParameter('followupVolumeID')
    if baselineVolumeID != None:
      self.__baselineVolumeSelector.setCurrentNode(slicer.util.getNode(baselineVolumeID))
    if followupVolumeID != None:
      self.__followupVolumeSelector.setCurrentNode(slicer.util.getNode(followupVolumeID))
