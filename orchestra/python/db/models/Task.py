__all__=['Task']


from sqlalchemy import Column, Integer, String, Date, Float, Boolean, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from orchestra.db.models import Base, Job
from orchestra.db.models.Worker import db
import datetime

#
#   Tasks Table
#
class Task (Base, db.Model):
  __tablename__ = 'task'

  # Local
  id = Column(Integer, primary_key = True)
  taskName = Column(String, unique=True)

  inputFilePath = Column(String)
  outputFilePath = Column(String)
  configFilePath = Column(String)
  containerImage = Column(String)

  # For LPS grid
  templateExecArgs   = Column( String, default="" )

  # Useful for extra data paths
  secondaryDataPath = Column( JSON, default="{}" )


  # For task status
  status = Column(String, default="registered")
  cluster = Column( String )

  queueName = Column( String )

  # Foreign
  jobs = relationship("Job", order_by="Job.id", back_populates="task")
  userId = Column(Integer, ForeignKey('worker.id'))
  user = relationship("Worker", back_populates="tasks")


  # For tinger staff
  etBinIdx  = Column( Integer )
  etaBinIdx = Column( Integer )


  # Signal column to be user to retry, delete or kill functions
  signal = Column( String, default='waiting' )

  timer = Column(DateTime)


  def __repr__ (self):
    return "<Task (taskName='{}', etBinIdx={}, etaBinIdx={}, jobs='{}', queue = {})>".format(
        self.taskName, self.etBinIdx, self.etaBinIdx, self.jobs, self.queueName)

  # Method that adds jobs into task
  def addJob (self, job):
    self.jobs.append(job)


  # Method that gets all jobs from task
  def getAllJobs (self):
    return self.jobs


  # Method that gets single task from user
  def getJob (self, configId):
    try:
      for job in self.jobs:
        if job.configId == configId:
          return job
      return None
    except:
      return None



  def getStatus(self):
    return self.status

  def setStatus(self,status):
    self.status = status


  def setTaskName(self, value):
    self.taskName = value

  def getTaskName(self):
    self.taskName


  def setCluster( self, name ):
    self.cluster = name

  def getCluster( self ):
    return self.cluster


  def setTemplateExecArgs(self, value):
    self.templateExecArgs = value

  def getTemplateExecArgs(self):
    return self.templateExecArgs


  def getContainerImage(self):
    return self.containerImage


  def getSignal(self):
    return self.signal

  def setSignal(self, value):
    self.signal = value


  def getUser(self):
    return self.user


  def startTimer(self):
    self.timer = datetime.datetime.now()


  def resetTimer(self):
    self.startTimer()


  def getTimer(self):
    return (datetime.datetime.now() - self.timer)


  def getQueueName(self):
    return self.queueName




