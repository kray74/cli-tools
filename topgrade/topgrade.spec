%global debug_package %{nil}

Name: topgrade
Version: 17.6.2
Release: 1%{?dist}
Summary: Upgrade all the things
License: GPL-3.0-or-later
URL: https://github.com/topgrade-rs/topgrade
Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: cargo
BuildRequires: rust

%description
Keeping your system up-to-date usually involves invoking multiple package
managers. This results in big, non-portable shell one-liners saved in your
shell. To remedy this, Topgrade detects which tools you use and runs the
appropriate commands to update them.

%prep
%autosetup

%build
cargo build --release --locked --config profile.release.strip=true
mkdir target/assets
target/release/%{name} --gen-manpage > target/assets/%{name}.1
target/release/%{name} --gen-completion bash > target/assets/%{name}.bash
target/release/%{name} --gen-completion fish > target/assets/%{name}.fish
target/release/%{name} --gen-completion zsh > target/assets/_%{name}

%install
install -Dpm 0755 -t %{buildroot}%{_bindir}/ target/release/%{name}
install -Dpm 0644 -t %{buildroot}%{_mandir}/man1/ target/assets/%{name}.1
install -Dpm 0644 -t %{buildroot}%{bash_completions_dir}/ target/assets/%{name}.bash
install -Dpm 0644 -t %{buildroot}%{fish_completions_dir}/ target/assets/%{name}.fish
install -Dpm 0644 -t %{buildroot}%{zsh_completions_dir}/ target/assets/_%{name}

%check
cargo test --release --locked

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{bash_completions_dir}/%{name}.bash
%{fish_completions_dir}/%{name}.fish
%{zsh_completions_dir}/_%{name}

%changelog
* Thu Jun 25 2026 Vasiliy Biryukov <kray74vb@gmail.com> - 17.6.2-1
- chore(topgrade): update to 17.6.2

* Sat Jun 13 2026 Vasiliy Biryukov <kray74vb@gmail.com> - 17.6.1-1
- feat(topgrade): add topgrade package
