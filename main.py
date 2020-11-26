# This script is the main entry of the project
from load_balancer import LoadBalancer
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Run format: python3 main.py <number of requests>')
    else:
        req_num = int(sys.argv[1])
        
        if req_num >= 2499:
            
            count = req_num // 2499
            while req_num:
                
                _req_num = 2499

                if req_num < 2499:
                    _req_num = req_num
                else:
                    req_num -= _req_num

                # Create a config object for load balancer
                policy = None

                if 0 <= _req_num < 100:
                    policy = 'round robin'
                elif 100 <= _req_num < 500:
                    policy = 'radomized static'
                elif 500 <= _req_num < 1250:
                    policy = 'least connection'
                elif 1250 <= _req_num < 2500:
                    policy = 'weighted least connection'

                cfg = {
                    'host': 'http://localhost',
                    'main_endpoint': 'work',
                    'port': 5000,
                    'policy': policy,
                    'hosts_configuration': { 'emea': 1, 'us': 2, 'asia': 2},
                    'req_num': _req_num
                }

                load_balancer = LoadBalancer(cfg)
                load_balancer.run()

            print('Finished requests')
        else:

            # Create a config object for load balancer
            policy = None

            if 0 <= req_num < 100:
                policy = 'round robin'
            elif 100 <= req_num < 500:
                policy = 'radomized static'
            elif 500 <= req_num < 1250:
                policy = 'least connection'
            elif 1250 <= req_num < 2500:
                policy = 'weighted least connection'

            cfg = {
                'host': 'http://localhost',
                'main_endpoint': 'work',
                'port': 5000,
                'policy': policy,
                'hosts_configuration': { 'emea': 1, 'us': 2, 'asia': 2},
                'req_num': req_num
            }

            load_balancer = LoadBalancer(cfg)
            load_balancer.run()

            print('Finished requests')

