HOW to deploy
-------------

1. Prepare config files ``qagent.conf`` and ``qmaster.conf``
2. Prepare a host file for Ansible
3. Install Python. If using a Redhat-like system, it can be done with
   ::
      $ ansible-playbook -e restricted_hosts=only-two provisioning-on-nodes.yml
   
4. Deploy QULo:
   ::
      $ ansible-playbook install.yml
      
5. Start ``qmaster``
   ::

      $ ansible-plabook start-qmaster.yml

6. Start ``qagent``
   ::

      $ ansible-plabook start-qagent.yml

