%define major 1
%define libname %mklibname appimage %{major}
%define devname %mklibname appimage -d
# static lib used in cmake file, not delete!
%define sdevname %mklibname appimage -d -s

%define realversion %(echo -n $(echo %{version} |cut -d. -f1-3); [ -n "%(echo %{version} |cut -d. -f4-)" ] && echo -n "-%(echo %{version} |cut -d. -f4-)")

Summary:	Implements functionality for dealing with AppImage files
Name:		libappimage
Version:	1.0.4.5
Release:	14
License:	GPLv2+
Group:		Networking/File transfer
Url:		https://github.com/AppImage/libappimage
Source0:	https://github.com/AppImage/libappimage/archive/v%{version}/%{name}-%{realversion}.tar.gz
Patch0:		libappimage-1.0.4-5-clang16-gcc13.patch
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	vim
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(libarchive)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(squashfuse)
BuildRequires:	cmake(XdgUtils)
BuildRequires:	boost-devel

%description
This library is part of the AppImage project. It implements functionality for 
dealing with AppImage files. It is written in C++ and is using Boost.

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Implements functionality for dealing with AppImage files
Group:		System/Libraries
Provides:	%{name} = %{EVRD}
Requires:	xdg-utils-cxx

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
Requires:	pkgconfig(glib-2.0)
Requires:	pkgconfig(cairo)
Requires:	pkgconfig(fuse)
Requires:	pkgconfig(libarchive)
Requires:	pkgconfig(liblzma)
Requires:	pkgconfig(librsvg-2.0)
Requires:	pkgconfig(squashfuse)
Requires:	cmake(XdgUtils)
Requires:	boost-devel
%rename %{sdevname}

%description -n %{devname}
This library is part of the AppImage project. It implements functionality for 
dealing with AppImage files. It is written in C++ and is using Boost.

%files -n %{devname}
%{_libdir}/libappimage.so
%{_includedir}/appimage
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/
# These aren't static library versions of the same thing,
# but static helpers needed by libappimage users
%{_libdir}/*.a
#----------------------------------------------------------------------------

%prep
%autosetup -n %{name}-%{realversion} -p1
%cmake  -DBUILD_TESTING=OFF \
	-DUSE_SYSTEM_BOOST=ON \
	-DUSE_SYSTEM_XZ=ON \
	-DUSE_SYSTEM_SQUASHFUSE=ON \
	-DUSE_SYSTEM_XDGUTILS=ON \
	-DUSE_SYSTEM_LIBARCHIVE=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

# static lib used in cmake files, NOT delete!
#rm %{buildroot}/%{_libdir}/*.a ||:
sed -i 's,\/\/usr,\/,' %{buildroot}/%{_libdir}/pkgconfig/%{name}.pc
