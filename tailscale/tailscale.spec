%global debug_package %{nil}
%global daemon tailscaled

Name: tailscale
Version: 1.104.7
Release: 2%{?dist}
Summary: The easiest, most secure way to use WireGuard and 2FA
License: BSD-3-Clause
URL: https://github.com/tailscale/tailscale
Source: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: golang
BuildRequires: gawk, sed
BuildRequires: systemd-rpm-macros

%description
%{summary}.

%prep
%autosetup

%build
# Install required go version if system is too old
%global go_required 1.27.4
go_version=$(go version | awk '{print $3}' | sed 's/go//')
if [ "$(printf '%s\n' "$go_version" "%{go_required}" | sort -V | head -n1)" = "$go_version" ] &&
	[ "$goversion" != "%{go_required}" ]; then
	go install golang.org/dl/go%{go_required}@latest
	export PATH="$HOME/go/bin:$PATH"
	go%{go_required} download
	GO=go%{go_required}
else
	GO=go
fi

export LDFLAGS="-s -w \
	-X tailscale.com/version.longStamp=%{version} \
	-X tailscale.com/version.shortStamp=%{version}"
$GO build -buildmode=pie -trimpath -ldflags="${LDFLAGS}" -o build/%{name} ./cmd/%{name}
$GO build -buildmode=pie -trimpath -ldflags="${LDFLAGS}" -o build/%{daemon} ./cmd/%{daemon}

build/%{name} completion bash > build/%{name}.bash
build/%{name} completion fish > build/%{name}.fish
build/%{name} completion zsh > build/_%{name}

%install
install -Dpm 0755 -t %{buildroot}%{_bindir}/ build/%{name} build/%{daemon}
install -Dpm 0644 -t %{buildroot}%{bash_completions_dir}/ build/%{name}.bash
install -Dpm 0644 -t %{buildroot}%{fish_completions_dir}/ build/%{name}.fish
install -Dpm 0644 -t %{buildroot}%{zsh_completions_dir}/ build/_%{name}
install -dpm 0600 %{buildroot}%{_sharedstatedir}/%{name}
install -dpm 0600 %{buildroot}%{_localstatedir}/cache/%{name}

# prepare for merged sbin
sed -i "s/sbin/bin/g" cmd/%{daemon}/%{daemon}.service
# let tailscaled detect nftables
# https://tailscale.com/docs/features/firewall-mode#heuristic
sed -i "s/EnvironmentFile=.*/Environment=PORT=41641\nEnvironment=TS_DEBUG_FIREWALL_MODE=auto/" \
	cmd/%{daemon}/%{daemon}.service
sed -i 's/$FLAGS//g' cmd/%{daemon}/%{daemon}.service
install -Dpm 0644 -t %{buildroot}%{_unitdir}/ cmd/%{daemon}/%{daemon}.service

%post
%systemd_post %{daemon}.service

%preun
%systemd_preun %{daemon}.service

%postun
%systemd_postun_with_restart %{daemon}.service

%files
%license LICENSE PATENTS licenses/tailscale.md
%doc README.md
%{_bindir}/%{name}
%{_bindir}/%{daemon}
%{_unitdir}/%{daemon}.service
%{bash_completions_dir}/%{name}.bash
%{fish_completions_dir}/%{name}.fish
%{zsh_completions_dir}/_%{name}
%dir %{_sharedstatedir}/%{name}
%dir %{_localstatedir}/cache/%{name}

%changelog
* Sun Nov 15 2026 Vasiliy Biryukov <kray74vb@gmail.com> 1.104.7-2
- fix(tailscale): move go version check to the build time

* Sun Nov 15 2026 Vasiliy Biryukov <kray74vb@gmail.com> 1.104.7-1
- feat(tailscale): Conditionally download required go version. Update to 1.104.7

* Sat Oct 31 2026 Vasiliy Biryukov <kray74vb@gmail.com> 1.104.4-1
- chore(tailscale): update to 1.104.4

* Sat Oct 24 2026 Vasiliy Biryukov <kray74vb@gmail.com> 1.104.2-1
- chore(tailscale): update to 1.104.2

* Sat Oct 3 2026 Vasiliy Biryukov <kray74vb@gmail.com> 1.102.5-1
- chore(tailscale): update to 1.102.5

* Sat Sep 12 2026 Vasiliy Biryukov <kray74vb@gmail.com> 1.102.4-1
- chore(tailscale): update to 1.102.4

* Sat Aug 22 2026 Vasiliy Biryukov <kray74vb@gmail.com> 1.102.3-1
- chore(tailscale): update to 1.102.3

* Sun Aug 9 2026 Vasiliy Biryukov <kray74vb@gmail.com> 1.102.2-1
- chore(tailscale): update to 1.102.2

* Sat Aug 1 2026 Vasiliy Biryukov <kray74vb@gmail.com> 1.98.10-1
- chore(tailscale): update to 1.98.10

* Sat Jul 25 2026 Vasiliy Biryukov <kray74vb@gmail.com> 1.98.9-1
- chore(tailscale): update to 1.98.9

* Sat Jul  4 2026 Vasiliy Biryukov <kray74vb@gmail.com> 1.98.8-1
- chore(tailscale): update to 1.98.8

* Sun Jun 14 2026 Vasiliy Biryukov <kray74vb@gmail.com> 1.98.5-2
- fix(tailscale): tailscaled.service must use /bin/tailscaled with sane defaults

* Sun Jun 14 2026 Vasiliy Biryukov <kray74vb@gmail.com> 1.98.5-1
- feat(tailscale): add tailscale package
