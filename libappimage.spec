%define major 1
%define libname %mklibname appimage %{major}
%define devname %mklibname appimage -d
# static lib used in cmake file, not delete!
%define sdevname %mklibname appimage -d -s

%define _disable_ld_no_undefined 1
%define realversion 1.0.4-5

Summary:	Implements functionality for dealing with AppImage files
Name:		libappimage
Version:	1.0.4.5
Release:	1
License:	GPLv2+
Group:		Networking/File transfer
Url:		https://github.com/AppImage/libappimage
Source0:	https://github.com/AppImage/libappimage/archive/v%{version}/%{name}-%{realversion}.tar.gz
BuildRequires:	cmake
BuildRequires:	vim
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(libarchive)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(squashfuse)
BuildRequires:	cmake(XdgUtils)
BuildRequires:	xdg-utils-cxx
BuildRequires:	boost-devel

%description
This library is part of the AppImage project. It implements functionality for 
dealing with AppImage files. It is written in C++ and is using Boost.

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Implements functionality for dealing with AppImage files
Group:		System/Libraries
Provides:	%{name} = %{EVRD}

%description -n %{libname}
This library is part of the AppImage project. It implements functionality for 
dealing with AppImage files. It is written in C++ and is using Boost.

%files -n %{libname}
%{_libdir}/libappimage.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Implements functionality for dealing with AppImage files
Group:		Development/C++
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
This library is part of the AppImage project. It implements functionality for 
dealing with AppImage files. It is written in C++ and is using Boost.

%files -n %{devname}
%{_libdir}/libappimage.so
%{_includedir}/appimage
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/
#----------------------------------------------------------------------------

%package -n %{sdevname}
Summary:	Libappimage development files (static library)
Group:		Development/Other
Requires:	%{devname} = %{EVRD}
Provides:	%{name}-static-devel = %{EVRD}

%description -n %{sdevname}
libappimage development files (static library).

%files -n %{sdevname}
%{_libdir}/*.a
#----------------------------------------------------------------------------

%prep
%autosetup -n %{name}-%{realversion} -p1

%build
%global ldflags %{ldflags} -Wl,-z,notext
%global ldflags %{ldflags} -fuse-ld=gold
%cmake  -DBUILD_TESTING=OFF \
	-DUSE_SYSTEM_BOOST=ON \
	-DUSE_SYSTEM_XZ=ON \
	-DUSE_SYSTEM_SQUASHFUSE=ON \
	-DUSE_SYSTEM_XDGUTILS=ON \
	-DUSE_SYSTEM_LIBARCHIVE=ON
%make

%install
%make_install -C build

# static lib used in cmake files, NOT delete!
#rm %{buildroot}/%{_libdir}/*.a ||:
sed -i 's,\/\/usr,\/,' %{buildroot}/%{_libdir}/pkgconfig/%{name}.pc
