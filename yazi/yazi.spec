%global debug_package %{nil}
%global yazicli ya

Name: yazi
Version: 26.5.6
Release: 1%{?dist}
Summary: Blazing fast terminal file manager written in Rust, based on async I/O
License: MIT
URL: https://github.com/sxyazi/yazi
Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: curl

Recommends: ffmpeg
Recommends: 7zip
Recommends: jq
Recommends: poppler-utils
Recommends: fd-find
Recommends: ripgrep
Recommends: fzf
Recommends: zoxide
Recommends: resvg
Recommends: ImageMagick

%description
Yazi (means "duck") is a terminal file manager written in Rust, based on
non-blocking async I/O. It aims to provide an efficient, user-friendly,
and customizable file management experience.

%prep
%autosetup

# system rust is too old (1.95.0 required)
bash <(curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs) --profile=minimal -y

%build
. "$HOME/.cargo/env"
export YAZI_GEN_COMPLETIONS=1
cargo build --release --locked

%install
install -Dpm 0755 -t %{buildroot}%{_bindir}/ target/release/%{name} target/release/%{yazicli}
install -Dpm 0644 -t %{buildroot}%{bash_completions_dir}/ yazi-boot/completions/%{name}.bash yazi-cli/completions/%{yazicli}.bash
install -Dpm 0644 -t %{buildroot}%{fish_completions_dir}/ yazi-boot/completions/%{name}.fish yazi-cli/completions/%{yazicli}.fish
install -Dpm 0644 -t %{buildroot}%{zsh_completions_dir}/ yazi-boot/completions/_%{name} yazi-cli/completions/_%{yazicli}

%check
. "$HOME/.cargo/env"
cargo test --workspace --release --locked

%files
%license LICENSE LICENSE-ICONS
%doc README.md
%{_bindir}/{%{name},%{yazicli}}
%{bash_completions_dir}/{%{name},%{yazicli}}.bash
%{fish_completions_dir}/{%{name},%{yazicli}}.fish
%{zsh_completions_dir}/_{%{name},%{yazicli}}

%changelog
* Mon Jun 15 2026 Vasiliy Biryukov <kray74vb@gmail.com> - 26.5.6-1
- feat(yazi): add yazi package
