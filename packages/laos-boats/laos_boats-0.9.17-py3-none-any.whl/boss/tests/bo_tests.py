import unittest
import numpy as np
from scipy.spatial.distance import euclidean


class BoTest(unittest.TestCase):
   
    #def tearDown(self):
        # Remove output and rst files


    def test0_add_get_xy(self):
        """
        Test adding and getting data in BoMain class
        """
        testTimer = Timer()
        settings = STS('inputs/methods.in', testTimer)

        bo = BoMain(settings, MainOutput(settings), RstManager(settings))

        x0 = ...
        y0 = ...

        bo.add_xy_list(x0, y0)

        x1 = bo.get_x()
        y1 = bo.get_y()
        
        # initialized model should contain only x0, y0 as data
        self.assertTrue(np.all(x1 == x0))
        self.assertAlmostEqual(y1, y0)


    def test0_init_model(self):
        """
        Test adding and getting data in BoMain class
        """
        testTimer = Timer()
        settings = STS('inputs/methods.in', testTimer)

        bo = BoMain(settings, MainOutput(settings), RstManager(settings))
        
        # initialize model by adding all initial points in input file
        bo.run_optimization()

        # model should be initialized
        self.assertNotEqual(bo.model, None)
        
        x0 = bo.get_x()
        y0 = bo.get_y()
        mu = bo.get_mu(x)

        # model should predict approximately mu == y0 at x0
        self.assertAlmostEqual(mu, y0)


    def test1_hartmann3(self):
        """
        Test whether BO class predicts the global minimum of hartmann-3
        function accurately (bounds=(0,1) for each component of x)
        """
        testTimer = Timer()
        settings = STS('inputs/hartmann3.in', testTimer)
        bo = BoMain(settings, MainOutput(settings), RstManager(settings))

        bo.run_optimization()

        # true global minimum 
        x_true = np.array([0.114614, 0.555649, 0.852547])
        y_true = -3.86278

        # BO global minimum prediction
        res = bo.convergence[-1]
        xhat = res[2]
        mu = res[3]

        # prediction should be close to true value
        self.assertAlmostEqual(euclidean(x_true, xhat), 0, places=4)
        self.assertAlmostEqual(mu, y0, places=4)


    def test2_hartmann6(self):
        """
        Test whether BO class predicts the global minimum of hartmann-6
        function accurately (bounds=(0,1) for each component of x)
        """
        testTimer = Timer()
        settings = STS('inputs/hartmann6.in', testTimer)
        bo = BoMain(settings, MainOutput(settings), RstManager(settings))

        bo.run_optimization()

        # true global minimum 
        x_true = np.array([0.20169, 0.150011, 0.476874, 0.275332, 0.311652,
        0.6573])
        y_true = -3.32237

        # BO global minimum prediction
        res = bo.convergence[-1]
        xhat = res[2]
        mu = res[3]
 
        # prediction should be close to true value
        self.assertAlmostEqual(euclidean(x_true, xhat), 0, places=4)
        self.assertAlmostEqual(mu, y0, places=4)


if __name__ == '__main__':
    unittest.main()

