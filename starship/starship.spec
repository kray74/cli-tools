%global debug_package %{nil}

Name: starship
Version: 1.25.1
Release: 1%{?dist}
Summary: The minimal, blazing-fast, and infinitely customizable prompt for any shell

License: ISC
URL: https://github.com/starship/starship
Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: cargo
BuildRequires: rust

# for tests
BuildRequires: git-core

%description
%{summary}.

%prep
%autosetup

%build
cargo build --release --locked

%install
install -Dpm 0755 -t %{buildroot}%{_bindir}/ target/release/%{name}

%check
cargo test --release --locked

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}

%changelog
* Sun Jun 07 2026 Vasiliy Biryukov <kray74vb@gmail.com> - 1.25.1-1
- feat(starship): add starship package
