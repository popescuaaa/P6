> popescuaaa 2020


[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs) [![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)  



# P6
## Description
P6 stands for Policies 6 and it's a very basic load balancer that allows multiple cofigurations via config files. The main purpose is to simulate and evaluate the performance of the policies in specific cases with a fixed number of client requests represented as a number, also part of the config file.

## Capabilities
The project was implemented in two main parts:
### Source code
1. The load balancer has a number of 6 different load balacing policies that can be set from the config file.
    - The main idea of the implementation is that in 'production' we should not stick on a single load balacing technique and we should choose the most suitable one based on the system state and based on the number of requests.
### Tester
2. Perform verbose log informations, errors and warnings if the servers don't responsd in a time limit. 
3. Gather and analyze all the data from requests to calculate different stats for a better policy comparation.

