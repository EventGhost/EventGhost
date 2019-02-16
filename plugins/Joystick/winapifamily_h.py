# Copyright (c) Microsoft Corporation. All rights reserved.
# Module Name:
#    winapifamily.h
# Abstract:
#     Master include file for API family partitioning.

from win_constants_h import *

_INC_WINAPIFAMILY = None
MOFCOMP_PASS = None
WINAPI_FAMILY = None
WINAPI_PARTITION_DESKTOP = None
WINAPI_PARTITION_APP = None
WINAPI_PARTITION_PC_APP = None
WINAPI_PARTITION_PHONE_APP = None
WINAPI_PARTITION_SYSTEM = None
WINAPI_PARTITION_SERVER = None

if not defined(_INC_WINAPIFAMILY):
    _INC_WINAPIFAMILY = 1

    if defined(_MSC_VER) and not defined(MOFCOMP_PASS):
        if _MSC_VER >= 1200:
            pass
        # ENDIF _MSC_VER >= 1200
    # ENDIF defined(_MSC_VER) and not defined(MOFCOMP_PASS)

    # When compiling C and C++ code using SDK header files, the development
    # environment can specify a target platform by #define-ing the
    # pre-processor symbol WINAPI_FAMILY to one of the following values.
    # Each FAMILY value denotes an application family for which a different
    # subset of the total set of header-file-defined APIs are available.
    # Setting the WINAPI_FAMILY value will effectively hide from the
    # editing and compilation environments the existence of APIs that
    # are not applicable to the family of applications targeting a
    # specific platform.

    # In Windows 10, WINAPI_PARTITIONs will be used to add additional
    # device specific APIs to a particular WINAPI_FAMILY.
    # For example, when writing Windows Universal apps, specifying
    # WINAPI_FAMILY_APP will hide phone APIs from compilation.
    # However, specifying WINAPI_PARTITION_PHONE_APP=1 additionally, will
    # unhide any API hidden behind the partition, to the compiler.

    # The following partitions are currently defined:

    # usable for Desktop Win32 apps (but not store apps)
    # WINAPI_PARTITION_DESKTOP

    # usable for Windows Universal store apps
    # WINAPI_PARTITION_APP

    # specific to Desktop-only store apps
    # WINAPI_PARTITION_PC_APP

    # specific to Phone-only store apps
    # WINAPI_PARTITION_PHONE_APP

    # specific to System applications
    # WINAPI_PARTITION_SYSTEM

    # The following partitions are indirect partitions and defined in
    # winpackagefamily.h. These partitions are related to package based
    # partitions. For example, specifying WINAPI_PARTITION_SERVER=1 will
    # light up
    # any API hidden behind the package based partitions that are bound to
    # WINAPI_PARTITION_SERVER, to the compiler.
    # WINAPI_PARTITION_SERVER             // specific to Server applications

    # The WINAPI_FAMILY values of 0 and 1 are reserved to ensure that
    # an error will occur if WINAPI_FAMILY is set to any
    # WINAPI_PARTITION value (which must be 0 or 1, see below).

    WINAPI_FAMILY_PC_APP = 2 # Windows Store Applications
    WINAPI_FAMILY_PHONE_APP = 3 # Windows Phone Applications
    WINAPI_FAMILY_SYSTEM = 4 # Windows Drivers and Tools
    WINAPI_FAMILY_SERVER = 5 # Windows Server Applications
    WINAPI_FAMILY_DESKTOP_APP = 100 # Windows Desktop Applications

    # The value of WINAPI_FAMILY_DESKTOP_APP may change in future SDKs.
    # Additional WINAPI_FAMILY values may be defined in future SDKs.

    #
    # For compatibility with Windows 8 header files, the following
    # synonym for WINAPI_FAMILY_PC_APP is temporarily #define'd.
    # Use of this symbol should be considered deprecated.
    #

    WINAPI_FAMILY_APP = WINAPI_FAMILY_PC_APP

    # If no WINAPI_FAMILY value is specified, then all APIs available to
    # Windows desktop applications are exposed.
    #

    if not defined(WINAPI_FAMILY):
        WINAPI_FAMILY = WINAPI_FAMILY_DESKTOP_APP
    # ENDIF defined(WINAPI_FAMILY)

    # API PARTITONs are part of an indirection mechanism for mapping between
    # individual APIs and the FAMILYs to which they apply.
    # Each PARTITION is a category or subset of named APIs.  PARTITIONs
    # are permitted to have overlapping membership -- some single API
    # might be part of more than one PARTITION.  PARTITIONS are each #define-ed
    # to be either 1 or 0 or depending on the platform at which the app is
    # targeted.

    # The mapping between families and partitions is summarized here.
    # An X indicates that the given partition is active for the given
    # platform/family.
    #
    #                                +-------------------+---+
    #                                |      *Partition*  |   |
    #                                +---+---+---+---+---+---+
    #                                |   |   |   |   |   |   |
    #                                |   |   |   |   |   |   |
    #                                |   |   |   | P |   |   |
    #                                |   |   |   | H |   |   |
    #                                | D |   |   | O |   |   |
    #                                | E |   | P | N | S | S |
    #                                | S |   | C | E | Y | E |
    #                                | K |   | _ | _ | S | R |
    #                                | T | A | A | A | T | V |
    # +-------------------------+----+ O | P | P | P | E | E |
    # |     *Platform/Family*       \| P | P | P | P | M | R |
    # +------------------------------+---+---+---+---+---+---+
    # | WINAPI_FAMILY_DESKTOP_APP    | X | X | X |   |   |   |
    # +------------------------------+---+---+---+---+---+---+
    # |      WINAPI_FAMILY_PC_APP    |   | X | X |   |   |   |
    # +------------------------------+---+---+---+---+---+---+
    # |   WINAPI_FAMILY_PHONE_APP    |   | X |   | X |   |   |
    # +----------------------------- +---+---+---+---+---+---+
    # |      WINAPI_FAMILY_SYSTEM    |   |   |   |   | X |   |
    # +----------------------------- +---+---+---+---+---+---+
    # |      WINAPI_FAMILY_SERVER    |   |   |   |   | X | X |
    # +------------------------------+---+---+---+---+---+---+

    # The table above is encoded in the following expressions,
    # each of which evaluates to 1 or 0.

    # Whenever a new family is added, all of these expressions
    # need to be reconsidered.

    if WINAPI_FAMILY not in (
        WINAPI_FAMILY_DESKTOP_APP,
        WINAPI_FAMILY_PC_APP,
        WINAPI_FAMILY_PHONE_APP,
        WINAPI_FAMILY_SYSTEM,
        WINAPI_FAMILY_SERVER
    ):
        raise RuntimeError(
            'Unknown WINAPI_FAMILY value. Was it defined '
            'in terms of a WINAPI_PARTITION_* value?'
        )
    # ENDIF WINAPI_FAMILY not in (
    #   WINAPI_FAMILY_DESKTOP_APP,
    #   WINAPI_FAMILY_PC_APP,
    #   WINAPI_FAMILY_PHONE_APP,
    #   WINAPI_FAMILY_SYSTEM ,
    #   WINAPI_FAMILY_SERVER
    # )

    if not defined(WINAPI_PARTITION_DESKTOP):
        WINAPI_PARTITION_DESKTOP = (
            WINAPI_FAMILY == WINAPI_FAMILY_DESKTOP_APP
        )
    # ENDIF not defined(WINAPI_PARTITION_DESKTOP)

    if not defined(WINAPI_PARTITION_APP):
        WINAPI_PARTITION_APP = (
            WINAPI_FAMILY in
            (
                WINAPI_FAMILY_DESKTOP_APP,
                WINAPI_FAMILY_PC_APP,
                WINAPI_FAMILY_PHONE_APP
            )
        )
    # ENDIF not defined(WINAPI_PARTITION_APP)

    if not defined(WINAPI_PARTITION_PC_APP):
        WINAPI_PARTITION_PC_APP = (
            WINAPI_FAMILY in (WINAPI_FAMILY_DESKTOP_APP, WINAPI_FAMILY_PC_APP)
        )
    # ENDIF not defined(WINAPI_PARTITION_PC_APP)

    if not defined(WINAPI_PARTITION_PHONE_APP):
        WINAPI_PARTITION_PHONE_APP = (
            WINAPI_FAMILY == WINAPI_FAMILY_PHONE_APP
        )

        WINAPI_PARTITION_PHONE_RESTRICTED = 0
    # ENDIF not defined(WINAPI_PARTITION_PHONE_APP)

    # SYSTEM is the only partition defined here.
    # All other System based editions are defined as packages
    # on top of the System partition.
    # See winpackagefamily.h for packages level partitions

    if not defined(WINAPI_PARTITION_SYSTEM):
        WINAPI_PARTITION_SYSTEM = (
            WINAPI_FAMILY in (WINAPI_FAMILY_SYSTEM, WINAPI_FAMILY_SERVER)
        )
    # ENDIF not defined(WINAPI_PARTITION_SYSTEM)

    # For compatibility with Windows Phone 8 header files, the following
    # synonym for WINAPI_PARTITION_PHONE_APP is temporarily #define'd.
    # Use of this symbol should be regarded as deprecated.

    WINAPI_PARTITION_PHONE = WINAPI_PARTITION_PHONE_APP

    # Header files use the WINAPI_FAMILY_PARTITION macro to assign one or
    # more declarations to some group of partitions.  The macro chooses
    # whether the preprocessor will emit or omit a sequence of declarations
    # bracketed by an #if/#endif pair.  All header file references to the
    # WINAPI_PARTITION_* values should be in the form of occurrences of
    # WINAPI_FAMILY_PARTITION(...).

    def WINAPI_FAMILY_PARTITION(Partitions):
         return Partitions

    # Macro used to #define or typedef a symbol used for selective deprecation
    # of individual methods of a COM interfaces that are otherwise available
    # for a given set of partitions.

    def _WINAPI_DEPRECATED_DECLARATION():
        raise RuntimeError(
            "This API cannot be used in the context"
            "of the caller's application type."
        )

    # For compatibility with Windows 8 header files, the following
    # symbol is temporarily conditionally #define'd.  Additional symbols
    # like this should be not defined in winapifamily.h, but rather should be
    # introduced locally to the header files of the component that needs them.

    if (
        WINAPI_FAMILY_PARTITION(WINAPI_PARTITION_APP) and
        not WINAPI_FAMILY_PARTITION(WINAPI_PARTITION_DESKTOP)
    ):
        APP_DEPRECATED_HRESULT = _WINAPI_DEPRECATED_DECLARATION
    # ENDIF (
    #     WINAPI_FAMILY_PARTITION(WINAPI_PARTITION_APP) and
    #     not WINAPI_FAMILY_PARTITION(WINAPI_PARTITION_DESKTOP)
    # )

    if defined(_MSC_VER) and not defined(MOFCOMP_PASS):
        if _MSC_VER >= 1200:
            pass
        # ENDIF if _MSC_VER >= 1200
    # ENDIF defined(_MSC_VER) and not defined(MOFCOMP_PASS)

    from winpackagefamily_h import *  # NOQA

# ENDIF not defined(_INC_WINAPIFAMILY)

__all__ = (
    'WINAPI_FAMILY_APP', 'WINAPI_FAMILY_DESKTOP_APP',
    'WINAPI_FAMILY_PARTITION', 'WINAPI_FAMILY_PC_APP',
    'WINAPI_FAMILY_PHONE_APP', 'WINAPI_FAMILY_SERVER',
    'WINAPI_FAMILY_SYSTEM', 'WINAPI_PARTITION_PHONE',
    '_WINAPI_DEPRECATED_DECLARATION', 'WINAPI_PARTITION_PHONE_RESTRICTED',
    'WINAPI_FAMILY', 'WINAPI_PARTITION_DESKTOP', 'WINAPI_PARTITION_APP',
    'WINAPI_PARTITION_PC_APP', 'WINAPI_PARTITION_PHONE_APP',
    'WINAPI_PARTITION_SYSTEM', 'WINAPI_PARTITION_SERVER',
)
