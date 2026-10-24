%global debug_package %{nil}

Name: starship
Version: 1.27.0
Release: 2%{?dist}
Summary: The minimal, blazing-fast, and infinitely customizable prompt for any shell

License: ISC
URL: https://github.com/starship/starship
Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

#BuildRequires: cargo
#BuildRequires: rust
BuildRequires: curl
BuildRequires: gcc
BuildRequires: tzdata

# for tests
BuildRequires: git-core

%description
%{summary}.

%prep
%autosetup

# system rust is too old (1.95.0 required)
bash <(curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs) --profile=minimal -y

%build
. "$HOME/.cargo/env"
cargo build --release --locked

%install
install -Dpm 0755 -t %{buildroot}%{_bindir}/ target/release/%{name}

%check
. "$HOME/.cargo/env"
cargo test --release --locked

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}

%changelog
* Sat Oct 24 2026 Vasiliy Biryukov <kray74vb@gmail.com> - 1.27.0-2
- fix(starship): add gcc dependency

* Sat Oct 24 2026 Vasiliy Biryukov <kray74vb@gmail.com> - 1.27.0-1
- chore(starship): update to 1.27.0

* Tue Jun 30 2026 Vasiliy Biryukov <kray74vb@gmail.com> - 1.26.0-2
- fix(starship): tzdata package is required for tests

* Tue Jun 30 2026 Vasiliy Biryukov <kray74vb@gmail.com> - 1.26.0-1
- chore(starship): update to 1.26.0

* Sun Jun 07 2026 Vasiliy Biryukov <kray74vb@gmail.com> - 1.25.1-1
- feat(starship): add starship package
