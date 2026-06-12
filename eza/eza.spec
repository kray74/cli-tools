%global debug_package %{nil}

Name: eza
Version: 0.23.4
Release: 1%{?dist}
Summary: Modern replacement for ls

License: EUPL-1.2
URL: https://github.com/eza-community/eza
Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: cargo
BuildRequires: rust
BuildRequires: pandoc

%description
eza is a modern alternative for the venerable file-listing command-line
program ls that ships with Unix and Linux operating systems, giving it more
features and better defaults. It uses colours to distinguish file types and
metadata. It knows about symlinks, extended attributes, and Git. And it’s
small, fast, and just one single binary.

By deliberately making some decisions differently, eza attempts to be a more
featureful, more user-friendly version of ls.

%prep
%autosetup

%build
cargo build --release --locked
mkdir target/man
for page in eza.1 eza_colors.5 eza_colors-explanation.5; do \
	sed "s/\$version/v%{version}/g" "man/${page}.md" | pandoc --standalone -f markdown -t man > "target/man/${page}"
done

%install
install -Dpm 0755 -t %{buildroot}%{_bindir}/ target/release/%{name}
install -Dpm 0644 -t %{buildroot}%{_mandir}/man1/ target/man/eza.1
install -Dpm 0644 -t %{buildroot}%{_mandir}/man5/ target/man/eza_colors.5
install -Dpm 0644 -t %{buildroot}%{_mandir}/man5/ target/man/eza_colors-explanation.5
install -Dpm 0644 -t %{buildroot}%{bash_completions_dir}/ completions/bash/%{name}
install -Dpm 0644 -t %{buildroot}%{fish_completions_dir}/ completions/fish/%{name}.fish
install -Dpm 0644 -t %{buildroot}%{zsh_completions_dir}/ completions/zsh/_%{name}

%check
cargo test --release --locked

%files
%license LICENSE.txt
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/eza.1*
%{_mandir}/man5/eza_colors*.5*
%{bash_completions_dir}/%{name}
%{fish_completions_dir}/%{name}.fish
%{zsh_completions_dir}/_%{name}

%changelog
* Fri Jun 12 2026 Vasiliy Biryukov <kray74vb@gmail.com> - 0.23.4-1
- feat(eza): add eza package
