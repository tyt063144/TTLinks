import subprocess


class FirewallTools:

    @staticmethod
    def filter_tcp_rst_by_sport(port):
        # Check if the rule already exists
        check_rule = ['iptables', '-C', 'OUTPUT', '-p', 'tcp', '--tcp-flags', 'RST', 'RST', '--sport', str(port), '-j', 'DROP']
        add_rule = ['iptables', '-A', 'OUTPUT', '-p', 'tcp', '--tcp-flags', 'RST', 'RST', '--sport', str(port), '-j', 'DROP']

        try:
            # Check for existing rule, add if it does not exist
            if subprocess.run(check_rule).returncode != 0:  # Rule does not exist
                subprocess.run(add_rule, check=True)
                print(f"Added iptables rule to drop RST packets on port {port}")
            else:
                print(f"Rule already exists for port {port}")
        except subprocess.CalledProcessError:
            print(f"Failed to add iptables rule for port {port}")

    @staticmethod
    def unfilter_tcp_rst_by_sport(port):
        remove_rule = ['iptables', '-D', 'OUTPUT', '-p', 'tcp', '--tcp-flags', 'RST', 'RST', '--sport', str(port), '-j', 'DROP']

        try:
            subprocess.run(remove_rule, check=True)
            print(f"Removed iptables rule to drop RST packets on port {port}")
        except subprocess.CalledProcessError:
            print(f"Failed to remove iptables rule for port {port} or rule does not exist")