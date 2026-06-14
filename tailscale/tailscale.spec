%global debug_package %{nil}
%global daemon tailscaled

Name: tailscale
Version: 1.98.5
Release: 1%{?dist}
Summary: The easiest, most secure way to use WireGuard and 2FA
License: BSD-3-Clause
URL: https://github.com/tailscale/tailscale
Source: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: golang
BuildRequires: systemd-rpm-macros

%description
%{summary}.

%prep
%autosetup

%build
export LDFLAGS="-s -w \
	-X tailscale.com/version.longStamp=%{version} \
	-X tailscale.com/version.shortStamp=%{version}"
go build -buildmode=pie -trimpath -ldflags="${LDFLAGS}" -o build/%{name} ./cmd/%{name}
go build -buildmode=pie -trimpath -ldflags="${LDFLAGS}" -o build/%{daemon} ./cmd/%{daemon}

build/%{name} completion bash > build/%{name}.bash
build/%{name} completion fish > build/%{name}.fish
build/%{name} completion zsh > build/_%{name}

%install
install -Dpm 0755 -t %{buildroot}%{_bindir}/ build/%{name} build/%{daemon}
install -Dpm 0644 -t %{buildroot}%{_unitdir}/ cmd/%{daemon}/%{daemon}.service
install -Dpm 0644 -t %{buildroot}%{bash_completions_dir}/ build/%{name}.bash
install -Dpm 0644 -t %{buildroot}%{fish_completions_dir}/ build/%{name}.fish
install -Dpm 0644 -t %{buildroot}%{zsh_completions_dir}/ build/_%{name}
install -dpm 0600 %{buildroot}%{_sharedstatedir}/%{name}
install -dpm 0600 %{buildroot}%{_localstatedir}/cache/%{name}

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
* Sun Jun 14 2026 Vasiliy Biryukov <kray74vb@gmail.com> 1.98.5-1
- feat(tailscale): add tailscale package
