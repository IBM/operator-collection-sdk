# Operator Collection SDK

# Overview
The Operator Collection SDK provides the resources and tools that are needed to develop Operator Collections against the IBM® z/OS® Cloud Broker which is part of the IBM Z® and Cloud Modernization Stack.

Operator Collections are simply [Ansible Collections](https://www.ansible.com/blog/getting-started-with-ansible-collections) that are dynamically converted to [Ansible Operators](https://www.ansible.com/blog/ansible-operator) in Openshift when imported in the [IBM® z/OS® Cloud Broker](https://ibm.biz/ibm-zoscb-install). This allows you to write any [Ansible Playbook](https://docs.ansible.com/ansible/2.9/user_guide/playbooks_intro.html), develop and iterate on it locally, publish to Openshift, and expose a catalog of statefully managed new services.

The Operator Collection SDK simplifies the development of these Operator Collections by providing:
- The ability to scaffold a new Operator Collection with a preconfigured set of requirements
- The ability to quickly debug your Ansible automation in an operator in Openshift, using a local build of your latest Ansible modifications

This project also provides the documented Operator Collection specification, along with a tutorial to guide you along the development process.



## Documentation Table of Contents
- [Operator Collection SDK](ibm/operator_collection_sdk/README.md)
- [Specification](docs/spec.md)
- [Tutorial](docs/tutorial.md)
- [Example Operator](examples/racf-operator/)
- [Lifecycle](docs/lifecycle.md)
  

## How to contribute
Check out the [contributor documentation](CONTRIBUTING.md).


## Copyright
© Copyright IBM Corporation 2023.