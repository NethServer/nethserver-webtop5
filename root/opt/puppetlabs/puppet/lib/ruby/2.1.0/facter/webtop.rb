# webtop.rb

require 'rubygems'

Facter.add('webtop') do
    setcode do
        webtop = {}
        pass = File.read("/var/lib/nethserver/secrets/webtop5").strip

        query_users = Facter::Core::Execution.exec("psql 'postgresql://sonicle:#{pass}@localhost:5432/webtop5' -Aqt -c \"select user_id from core.users where type = 'U' and user_id != 'admin'\"")
        actual_users = query_users.split("\n")

        query_provider = Facter::Core::Execution.exec("echo '{\"action\":\"list-users\"}' | /usr/bin/sudo /usr/libexec/nethserver/api/system-users/read | jq -r 'keys | .[]'")
        provider_user = query_provider.split("\n")

        webtop['users'] = (actual_users & provider_user).length

        for t in ['core.shares', 'calendar.calendars', 'contacts.contacts'] do
            out = Facter::Core::Execution.exec("psql 'postgresql://sonicle:#{pass}@localhost:5432/webtop5' -Aqt -c 'select count(*) from #{t}'")
            webtop[t.split('.')[1]] = out.to_i
        end
        pid = Facter::Core::Execution.exec("systemctl show tomcat8@webtop -p MainPID").strip().split("=")[1]
        if pid.to_i > 0
            File.open("/proc/#{pid}/status").each do |line|
                parts = line.split(":")
                label = parts[0].strip()
                value = parts[1].strip()
                if label == "VmSize"
                    webtop['memory_virtual'] = value.match(/(\d+)/)[1].to_i
                end
                if label == "VmRSS"
                    webtop['memory_resident'] = value.match(/(\d+)/)[1].to_i
                end
            end
        end

        agents = Facter::Core::Execution.exec("grep 'GET /webtop' /var/log/httpd/access_log | awk -F\\\" '{print $6}' | sort | uniq");
        webtop['agents'] = agents.split("\n");

        webtop
    end
end
