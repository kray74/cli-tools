%global debug_package %{nil}

Name: zoxide
Version: 0.9.9
Release: 1%{?dist}
Summary: Smarter cd command, inspired by z and autojump

License: MIT
URL: https://github.com/ajeetdsouza/zoxide
Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: cargo
BuildRequires: rust

Recommends: fzf

%description
zoxide remembers which directories you use most frequently,
so you can "jump" to them in just a few keystrokes.

%prep
%autosetup

%build
cargo build --release --locked

%install
install -Dpm 0755 -t %{buildroot}%{_bindir}/ target/release/%{name}
install -Dpm 0644 -t %{buildroot}%{_mandir}/man1/ man/man1/%{name}*.1
install -Dpm 0644 -t %{buildroot}%{bash_completions_dir}/ contrib/completions/%{name}.bash
install -Dpm 0644 -t %{buildroot}%{fish_completions_dir}/ contrib/completions/%{name}.fish
install -Dpm 0644 -t %{buildroot}%{zsh_completions_dir}/ contrib/completions/_%{name}

%check
cargo test --release --locked

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}*.1*
%{bash_completions_dir}/%{name}.bash
%{fish_completions_dir}/%{name}.fish
%{zsh_completions_dir}/_%{name}

%changelog
* Wed Jun 10 2026 Vasiliy Biryukov <kray74vb@gmail.com> - 0.9.9-1
- feat(zoxide): add zoxide package
