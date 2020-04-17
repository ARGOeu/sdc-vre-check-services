Name:           sdc-vre-check-services
Version:        0.1
Release:        1%{?dist}
Summary:        Nagios probe for SDC VRE Services
License:        GPLv3+
Packager:       Themis Zamani <themiszamani@gmail.com>

Source:         %{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}
AutoReqProv: no

%description
Nagios probe to check health of VRE Services

%prep
%setup -q

%define _unpackaged_files_terminate_build 0

%install

install -d %{buildroot}/%{_libexecdir}/argo-monitoring/probes/sdc-vre-check-services
install -d %{buildroot}/%{_sysconfdir}/nagios/plugins/sdc-vre-check-services
install -m 755 vre-check-services-health.py %{buildroot}/%{_libexecdir}/argo-monitoring/probes/sdc-vre-check-services/vre-check-services-health.py

%files
%dir /%{_libexecdir}/argo-monitoring
%dir /%{_libexecdir}/argo-monitoring/probes/
%dir /%{_libexecdir}/argo-monitoring/probes/sdc-vre-check-services

%attr(0755,root,root) /%{_libexecdir}/argo-monitoring/probes/sdc-vre-check-services/vre-check-services-health.py

%changelog
* Fri Apr 17 2020 Themis Zamani  <themiszamani@gmail.com> - 0.1-1
- Packaging

