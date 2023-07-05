# Epsilon greedy
Mini-project from Karpov.Courses studying

### Description
Purpose of the project is to implement service with bandit algorithm that allows to automatically determine advertising offer that will have the best CPA conversion for a given traffic from a wide group of differnet offers. Another part of the project is to make preparation for A/B test
Service must have 3 endpoints:
- First one gets click id and offers id list, choose and best offer for requested click id
- Second one gets click id and amount of reward from that click and update statistcs for related offer id
- Third one returns statistics for requested offer id

### Completed tasks
- Implement greedy algorithm to choose offer
- Implement ε-greedy algorithm to choose offer
- Implement one of main bandit algorithms to choose offer and reach minimal regret. I chose UCB and got about 15% regret according to grading system of the platform

- Implement class that separates users into groups
- Implement functions for A/A- and A/B-test on artificial CPC data and calculate sample size and MDE
