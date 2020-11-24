from load_balancer import LoadBalancer, POLICIES
from tests import *
import matplotlib.pyplot as pyplot
import yaml

if __name__ == "__main__":
    with open('config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    """
        Test general architecture capabilities
    """
    # 0
    init_testing_environment(config['general_architecture'])
    # 1
    requests_per_instance = requests_per_instance()
    # 2
    latency_per_region = latency_per_region()
    # 3
    work_time_per_region = work_time_per_region()
    # 4
    response_time_without_load = response_time_without_load()
    #5
    forwarding_unit_latency_estiamation = forwarding_unit_latency_estiamation()

    
    # load_balancer = LoadBalancer(config)
    # load_balancer.run()