%global debug_package %{nil}

Name: lazygit
Version: 0.66.3
Release: 1%{?dist}
Summary: Simple terminal UI for git commands
License: MIT
URL: https://github.com/jesseduffield/lazygit
Source: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

Requires: git-core

BuildRequires: golang
# for tests
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
go test -short -skip="TestFailingFixture" ./...

%files
%license LICENSE
%doc README.md docs/
%{_bindir}/%{name}

%changelog
* Sun Nov 15 2026 Vasiliy Biryukov <kray74vb@gmail.com> 0.66.3-1
- feat(lazygit): add git-core to dependencies. Update to 0.66.3

* Sat Oct 17 2026 Vasiliy Biryukov <kray74vb@gmail.com> 0.66.2-1
- chore(lazygit): update to 0.66.2

* Sat Oct 10 2026 Vasiliy Biryukov <kray74vb@gmail.com> 0.66.0-1
- chore(lazygit): update to 0.66.0

* Sat Sep 19 2026 Vasiliy Biryukov <kray74vb@gmail.com> 0.65.1-1
- chore(lazygit): update to 0.65.1

* Sat Sep 12 2026 Vasiliy Biryukov <kray74vb@gmail.com> 0.65.0-1
- chore(lazygit): update to 0.65.0

* Sat Aug 15 2026 Vasiliy Biryukov <kray74vb@gmail.com> 0.64.1-1
- chore(lazygit): update to 0.64.1

* Sun Aug 9 2026 Vasiliy Biryukov <kray74vb@gmail.com> 0.64.0-1
- chore(lazygit): update to 0.64.0

* Sat Jul 18 2026 Vasiliy Biryukov <kray74vb@gmail.com> 0.63.1-1
- chore(lazygit): update to 0.63.1

* Sat Jul 11 2026 Vasiliy Biryukov <kray74vb@gmail.com> 0.63.0-1
- chore(lazygit): update to 0.63.0

* Fri Jun 12 2026 Vasiliy Biryukov <kray74vb@gmail.com> 0.62.2-2
- fix(lazygit): add git-core build dependency required for tests

* Fri Jun 12 2026 Vasiliy Biryukov <kray74vb@gmail.com> 0.62.2-1
- feat(lazygit): add lazygit package
