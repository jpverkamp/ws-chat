#!/bin/bash

# http://www.raweng.com/blog/2014/11/11/websockets-on-aws-elb/

ELB_NAME = websocket-test

aws elb create-load-balancer-policy --load-balancer-name $ELB_NAME --policy-name $ELB_NAME-proxy-protocol –policy-type-name ProxyProtocolPolicyType --policy-attributes AttributeName=ProxyProtocol,AttributeValue=True

aws elb set-load-balancer-policies-for-backend-server --load-balancer-name $ELB_NAME --instance-port 80 --policy-names $ELB_NAME-proxy-protocol
