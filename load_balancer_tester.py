from load_balancer import LoadBalancer, POLICIES
import yaml

if __name__ == "__main__":
    with open('config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    """
        Test general architecture capabilities

    """
    load_balancer = LoadBalancer(config)
    load_balancer.run()