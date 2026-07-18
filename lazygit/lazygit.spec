%global debug_package %{nil}

Name: lazygit
Version: 0.63.1
Release: 1%{?dist}
Summary: Simple terminal UI for git commands
License: MIT
URL: https://github.com/jesseduffield/lazygit
Source: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: golang
BuildRequires: git-core

%description
%{summary}.

%prep
%autosetup

%build
go build -buildmode=pie -o bin/%{name} \
	-ldflags="-s -w -X main.version=%{version}"

%install
install -Dpm 0755 -t %{buildroot}%{_bindir}/ bin/%{name}

%check
go test -short ./...

%files
%license LICENSE
%doc README.md docs/
%{_bindir}/%{name}

%changelog
* Sat Jul 18 2026 Vasiliy Biryukov <kray74vb@gmail.com> 0.63.1-1
- chore(lazygit): update to 0.63.1

* Sat Jul 11 2026 Vasiliy Biryukov <kray74vb@gmail.com> 0.63.0-1
- chore(lazygit): update to 0.63.0

* Fri Jun 12 2026 Vasiliy Biryukov <kray74vb@gmail.com> 0.62.2-2
- fix(lazygit): add git-core build dependency required for tests

* Fri Jun 12 2026 Vasiliy Biryukov <kray74vb@gmail.com> 0.62.2-1
- feat(lazygit): add lazygit package
