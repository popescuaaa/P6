from load_balancer import LoadBalancer, POLICIES
from tests import *
import yaml
import sys

if __name__ == "__main__":
    with open('config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    print(len(sys.argv))
    if len(sys.argv) < 2:
        print('Usage: load_balancer_tester.py <arch> | <policies>')
    else:
        param = str(sys.argv[1])

    if param == 'arch':
        """
            Test general architecture capabilities
        """
        # 0
        cfg = config['general_architecture']
        # 1
        ga_rpi = 'ga_rpi.log'
        requests_per_instance = requests_per_instance(cfg)
        logfile = open(ga_rpi, "w")
        for e in requests_per_instance:
            logfile.write('Endpoint: {} limit: {}'.format(e, requests_per_instance[e][0]))
            logfile.write('\n')
            logfile.write(str(requests_per_instance[e][1]))
            logfile.write('\n')
        logfile.close()
        # 2
        # latency_per_region = latency_per_region(cfg)
        # ga_lpr = 'ga_lpr.log'
        # logfile = open(ga_lpr, "w")
        # for r in latency_per_region:
        #     logfile.write('Region: {} latency: {}'.format(r, latency_per_region[r]))
        #     logfile.write('\n')
        # logfile.close()
        # 3
        # work_time_per_region = work_time_per_region(cfg)
        # ga_wtpr = 'ga_wtpr.log'
        # logfile = open(ga_wtpr, "w")
        # for r in work_time_per_region:
        #     logfile.write('Region: {} work time: {}'.format(r, work_time_per_region[r]))
        #     logfile.write('\n')
        # logfile.close()
        # 4
        # response_time_without_load = response_time_without_load(cfg)
        # ga_rtwl = 'ga_rtwl.log'
        # logfile = open(ga_rtwl, "w")
        # for e in response_time_without_load:
        #     logfile.write('Endpoint: {} response time without load: {}'.format(e, response_time_without_load[e]))
        #     logfile.write('\n')
        # logfile.close()
        #5
        # forwarding_unit_latency_estiamation = forwarding_unit_latency_estiamation(cfg)
        # ga_fwle = 'ga_fwle.log'
        # logfile = open(ga_fwle, "w")
        # for r in forwarding_unit_latency_estiamation:
        #     logfile.write('Region: {} forward unit latency estimation: {}'.format(r, forwarding_unit_latency_estiamation[r]))
        #     logfile.write('\n')
        # logfile.close()

    elif param == 'policies':
        """
            Test load balancer policies compare them
        """
        rr_cfg = config['production_round_robin']
        print(rr_cfg)
        load_balancer = LoadBalancer(rr_cfg)
        load_balancer.run()

        wrr_cfg = config['production_weighted_round_robin']
        print(wrr_cfg)
        load_balancer = LoadBalancer(wrr_cfg)
        load_balancer.run()

        lc_cfg = config['production_least_connection']
        print(lc_cfg)
        load_balancer = LoadBalancer(lc_cfg)
        load_balancer.run()

        wlc_cfg = config['production_weighted_least_connection']
        print(wlc_cfg)
        load_balancer = LoadBalancer(wlc_cfg)
        load_balancer.run()

        fw_cfg = config['production_fixed_weighting']
        print(fw_cfg)
        load_balancer = LoadBalancer(fw_cfg)
        load_balancer.run()

        rs_cfg = config['production_randomized_static']
        print(rs_cfg)
        load_balancer = LoadBalancer(rs_cfg)
        load_balancer.run()


    else:
        print('Unsupported parameter for testing. Try: "arch" or "policies".')