%global debug_package %{nil}

Name: chezmoi
Version: 2.71.0
Release: 1%{?dist}
Summary: Manage your dotfiles across multiple diverse machines, securely
License: MIT
URL: https://github.com/twpayne/chezmoi
Source: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: golang
Recommends: git-core

%description
chezmoi helps you manage your personal configuration files
(dotfiles, like ~/.gitconfig) across multiple machines.

chezmoi provides many features beyond symlinking or using a bare git repo
including:
- templates (to handle small differences between machines)
- password manager support (to store your secrets securely)
- importing files from archives (great for shell and editor plugins)
- full file encryption (using age, gpg, git-crypt, or transcrypt)
- running scripts (to handle everything else).

%prep
%autosetup

%build
go build -buildmode=pie -o bin/%{name} -ldflags="-s -w \
	-X main.version=%{version} \
	-X main.date=$(date -u -I -d "@${SOURCE_DATE_EPOCH}")"

%install
install -Dpm 0755 -t %{buildroot}%{_bindir}/ bin/%{name}
install -Dpm 0644 completions/%{name}-completion.bash -t %{buildroot}%{bash_completions_dir}/%{name}.bash
install -Dpm 0644 -t %{buildroot}%{fish_completions_dir}/ completions/%{name}.fish
install -Dpm 0644 completions/%{name}.zsh -t %{buildroot}%{zsh_completions_dir}/_%{name}

%check
go test ./...

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{bash_completions_dir}/%{name}.bash
%{fish_completions_dir}/%{name}.fish
%{zsh_completions_dir}/_%{name}

%changelog
* Sat Jul 11 2026 Vasiliy Biryukov <kray74vb@gmail.com> 2.71.0-1
- chore(chezmoi): update to 2.71.0

* Sat Jun 13 2026 Vasiliy Biryukov <kray74vb@gmail.com> 2.70.5-2
- fix(chezmoi): remove time from --version output

* Sat Jun 13 2026 Vasiliy Biryukov <kray74vb@gmail.com> 2.70.5-1
- feat(chezmoi): add chezmoi package
