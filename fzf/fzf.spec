%global debug_package %{nil}

Name: fzf
Version: 0.73.1
Release: 2%{?dist}
Summary: Command line fuzzy finder
License: MIT
URL: https://github.com/junegunn/%{name}
Source: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: golang

%description
Interactive filter program for any kind of list;
files, command history, processes, hostnames, bookmarks, git commits, etc.
It implements a "fuzzy" matching algorithm, so you can quickly type in patterns
with omitted characters and still get the results you want.

%prep
%autosetup

%build
go build -buildmode=pie -o bin/%{name} \
	-ldflags="-s -w -X main.version=%{version} -X main.revision=cli-tools"

%install
install -Dpm 0755 -t %{buildroot}%{_bindir}/ bin/%{name} bin/%{name}-tmux
install -Dpm 0644 -t %{buildroot}%{_mandir}/man1 man/man1/%{name}.1 man/man1/%{name}-tmux.1

# Install in /etc instead of /usr/share
# See https://bugzilla.redhat.com/show_bug.cgi?id=1789958
install -Dpm 0644 shell/completion.bash %{buildroot}%{_sysconfdir}/bash_completion.d/fzf

install -Dpm 0644 shell/completion.fish %{buildroot}%{fish_completions_dir}/fzf.fish
install -Dpm 0644 shell/completion.zsh %{buildroot}%{zsh_completions_dir}/_fzf

%check
go test ./...

%files
%license LICENSE
%doc README.md ADVANCED.md doc/fzf.txt CHANGELOG.md
%{_bindir}/%{name}
%{_bindir}/%{name}-tmux
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}-tmux.1*
%{_sysconfdir}/bash_completion.d/fzf
%{fish_completions_dir}/fzf.fish
%{zsh_completions_dir}/_fzf

%changelog
* Mon Jun 08 2026 Vasiliy Biryukov <kray74vb@gmail.com> 0.73.1-2
- feat(fzf): remove go-rpm-macros facilities

* Sat Jun 06 2026 Vasiliy Biryukov <kray74vb@gmail.com> 0.73.1-1
- chore(fzf): update to 0.73.1

* Sun May 31 2026 Vasiliy Biryukov <kray74vb@gmail.com> 0.72.0-1
- feat(fzf): add fzf package
