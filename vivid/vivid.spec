%global debug_package %{nil}

Name: vivid
Version: 0.11.1
Release: 1%{?dist}
Summary: Themeable LS_COLORS generator with a rich filetype database
License: Apache-2.0 or MIT
URL: https://github.com/sharkdp/vivid
Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: cargo
BuildRequires: rust

%description
vivid is a generator for the LS_COLORS environment variable that controls
the colorized output of ls, tree, fd, bfs, dust and many other tools.

It uses a YAML configuration format for the filetype-database and the color
themes. In contrast to dircolors, the database and the themes are organized
in different files. This allows users to choose and customize color themes
independent from the collection of file extensions. Instead of using cryptic
ANSI escape codes, colors can be specified in the RRGGBB format and will be
translated to either truecolor (24-bit) ANSI codes or 8-bit codes for older
terminal emulators.

%prep
%autosetup

%build
cargo build --release --locked

%install
install -Dpm 0755 -t %{buildroot}%{_bindir}/ target/release/%{name}

%check
cargo test --release --locked

%files
%license LICENSE-APACHE LICENSE-MIT
%doc README.md
%{_bindir}/%{name}

%changelog
* Sun Jun 14 2026 Vasiliy Biryukov <kray74vb@gmail.com> - 0.11.1-1
- feat(vivid): add vivid package
