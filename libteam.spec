%define tmajor 5
%define libteam %mklibname team %{tmajor}
%define tdmajor 0
%define libtmdc %mklibname teamdctl %{tdmajor}
%define devname %mklibname team -d

Name:		libteam
Version:	1.31
Release:	2
Summary:	Library for controlling team network device
Group:		System/Libraries
License:	LGPLv2+
URL:		http://www.libteam.org
Source0:	http://www.libteam.org/files/%{name}-%{version}.tar.gz
Source1:	teamd_zmq_common.h
Patch0:		libteam-1.10-add-missing-libteamdctl-libdaemon-dependency.patch
BuildRequires:	pkgconfig(jansson)
BuildRequires:	pkgconfig(libdaemon)
BuildRequires:	pkgconfig(libnl-3.0)
BuildRequires:	pkgconfig(libzmq)
BuildRequires:	pkgconfig(python2)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	swig

%description
This package contains a library which is a user-space
counterpart for team network driver. It provides an API
to control team network devices.

%package -n teamnl
Summary:	team network device Netlink interface tool
Group:		System/Configuration/Networking

%description -n	teamnl
teamnl is a tool enabling interaction with a team device via the team driver
Netlink interface.
This tools serves mainly for debugging purposes.

%package -n %{libteam}
Summary:	Library for controlling team network device
Group:		System/Libraries

%description -n	%{libteam}
This package contains a library which is a user-space
counterpart for team network driver. It provides an API
to control team network devices.

%package -n %{devname}
Group:		Development/C
Summary:	Libraries and header files for libteam & teamd development
Requires:	teamnl = %{EVRD}
Requires:	%{libteam} = %{EVRD}
Requires:	%{libtmdc} = %{EVRD}

%description -n	%{devname}
This package contains the header files and libraries
necessary for developing programs using libteam & libteamdctl.

%package -n teamd
Group:		System/Configuration/Networking
Summary:	Team network device control daemon
Requires:	teamnl = %{EVRD}

%description -n teamd
The teamd package contains team network device control daemon.

%package -n %{libtmdc}
Summary:	Library for team network device control daemon
Group:		System/Libraries

%description -n	%{libtmdc}
This package contains a library which is a user-space
counterpart for team network driver. It provides an API
for the team network control daemon..

%package -n python2-libteam
Group:		Development/Python
Summary:	Team network device library bindings
Requires:	teamnl = %{EVRD}

%description -n python2-libteam
The team-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by team network device library.

This package should be installed if you want to develop Python
programs that will manipulate team network devices.

%prep
%setup -q
%patch0 -p1 -b .libdaemon~

# missing from tarball, fetched from git
cp %{SOURCE1} teamd/
# prepare example dir for -devel
mkdir -p _tmpdoc1/examples
cp -p examples/*.c _tmpdoc1/examples
# prepare example dir for team-python
mkdir -p _tmpdoc2/examples
cp -p examples/python/*.py _tmpdoc2/examples
chmod -x _tmpdoc2/examples/*.py

autoreconf -fsv

%build
export PYTHON=%{__python2}
%configure
%make
cd binding/python
%{__python2} ./setup.py build

%install
export PYTHON=%{__python2}
%makeinstall_std
install -p teamd/dbus/teamd.conf -D %{buildroot}%{_sysconfdir}/dbus-1/system.d/teamd.conf
install -p teamd/redhat/systemd/teamd@.service -D %{buildroot}%{_unitdir}/teamd@.service
install -p -m755 teamd/redhat/initscripts_systemd/network-scripts/ifup-Team -D %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifup-Team
install -p -m755 teamd/redhat/initscripts_systemd/network-scripts/ifdown-Team -D %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifdown-Team
install -p -m755 teamd/redhat/initscripts_systemd/network-scripts/ifup-TeamPort -D %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifup-TeamPort
install -p -m755 teamd/redhat/initscripts_systemd/network-scripts/ifdown-TeamPort -D %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifdown-TeamPort
install -p -m755 utils/bond2team -D %{buildroot}%{_bindir}/bond2team
cd binding/python
%{__python2} ./setup.py install --root %{buildroot} -O1

%files -n teamnl
%{_bindir}/teamnl
%{_mandir}/man8/teamnl.8*

%files -n %{libteam}
%{_libdir}/libteam.so.%{tmajor}*

%files -n %{devname}
%doc _tmpdoc1/examples
%{_includedir}/team.h
%{_includedir}/teamdctl.h
%{_libdir}/libteam.so
%{_libdir}/libteamdctl.so
%{_libdir}/pkgconfig/libteam.pc
%{_libdir}/pkgconfig/libteamdctl.pc

%files -n teamd
%doc teamd/example_configs teamd/redhat/example_ifcfgs/
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/dbus-1/system.d/teamd.conf
%attr(644,root,root) %{_unitdir}/teamd@.service
%{_sysconfdir}/sysconfig/network-scripts/ifup-Team
%{_sysconfdir}/sysconfig/network-scripts/ifdown-Team
%{_sysconfdir}/sysconfig/network-scripts/ifup-TeamPort
%{_sysconfdir}/sysconfig/network-scripts/ifdown-TeamPort
%{_bindir}/teamd
%{_bindir}/teamdctl
%{_bindir}/bond2team
%{_mandir}/man8/teamd.8*
%{_mandir}/man8/teamdctl.8*
%{_mandir}/man5/teamd.conf.5*
%{_mandir}/man1/bond2team.1*

%files -n %{libtmdc}
%{_libdir}/libteamdctl.so.%{tdmajor}*

%files -n python2-libteam
%doc _tmpdoc2/examples
%{python2_sitearch}/team-1.0-py%{py2_ver}.egg-info
%dir %{python2_sitearch}/team
%{python2_sitearch}/team/*
