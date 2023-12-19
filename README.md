# tseeb
A viewer for Ansible facts. (_tseeb_, Translated from Hmong)

## Get the Facts - CLI
- Command:
```
ANSIBLE_LOAD_CALLBACK_PLUGINS=true ANSIBLE_STDOUT_CALLBACK=json ansible all -m ansible.builtin.setup | tee /tmp/facts.json
```

- Creates:
```
/tmp/facts.json
```

## Get the Facts - Playbook
- Playbook (save in `roles/facts/tasks/main.yml`):
```
---
- name: Gather Server Facts and Write to File
  hosts: all
  gather_facts: true
  tasks:
    - name: Writing Facts
      ansible.builtin.copy:
        content: "{{ ansible_facts | to_nice_json }}"
        dest: /tmp/{{ inventory_hostname }}.json
    
    - name: Downloading Facts
      ansible.builtin.fetch:
        src: /tmp/{{ inventory_hostname }}.json
        dest: /tmp/facts/
```

- Command:
```
ansible-playbook roles/facts/tasks/main.yml
```

- Creates:
```
/tmp/facts/server-1.example.com/tmp/server-1.example.com.json
/tmp/facts/server-2.example.com/tmp/server-2.example.com.json
/tmp/facts/server-3.example.com/tmp/server-3.example.com.json
...
```
