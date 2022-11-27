import numpy as np

def calcLogArray(data):
		"""
        Take in an array of data and return a corresponding array of 
		log-returns for that data.

        Parameters
        ----------
        data : numpy.ndarray

        Returns
        -------
        numpy.ndarray
           array of log-returns
        """
		log_data = data[0:-1,:]
		for j in range(len(data) - 1):
			for i in range(len(data[0])):
				log_data[j][i] = np.log(data[j+1][i]/data[j][i])
		return log_data
		