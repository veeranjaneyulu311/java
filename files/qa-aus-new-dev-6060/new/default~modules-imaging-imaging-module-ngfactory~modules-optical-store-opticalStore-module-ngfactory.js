(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["default~modules-imaging-imaging-module-ngfactory~modules-optical-store-opticalStore-module-ngfactory"],{

/***/ "./src/app/modules/imaging/services/imaging.service.ts":
/*!*************************************************************!*\
  !*** ./src/app/modules/imaging/services/imaging.service.ts ***!
  \*************************************************************/
/*! exports provided: ImagingService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImagingService", function() { return ImagingService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _core_services_utils_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @core/services/utils.service */ "./src/app/core/services/utils.service.ts");
/* harmony import */ var aws_sdk_clients_s3__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! aws-sdk/clients/s3 */ "./node_modules/aws-sdk/clients/s3.js");
/* harmony import */ var aws_sdk_clients_s3__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(aws_sdk_clients_s3__WEBPACK_IMPORTED_MODULE_2__);



var ImagingService = /** @class */ (function () {
    function ImagingService(appConstants, SparkMD5, JSZip, utilService) {
        this.appConstants = appConstants;
        this.SparkMD5 = SparkMD5;
        this.JSZip = JSZip;
        this.utilService = utilService;
        this.CHUNK_SIZES = 2097152; // incremental hash chunk size
    }
    ImagingService.prototype.chartObjectFactory = function (seriesName) {
        return {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie',
                spacing: [0, 0, 0, 0],
                margin: [0, 0, 0, 0]
            },
            boost: {
                allowForce: true,
                useGPUTranslations: true
            },
            credits: {
                enabled: false
            },
            title: {
                text: null
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    colors: [
                        '#FF9655',
                        '#6AF9C4',
                        '#058DC7',
                        '#50B432',
                        '#ED561B',
                        '#DDDF00',
                        '#24CBE5',
                        '#64E572',
                        '#FFF263'
                    ],
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}:</b> {point.percentage:.1f} %',
                        style: {
                            textOutline: 0,
                            color: '#777',
                            fontSize: '10px'
                        },
                        distance: 10
                    }
                }
            },
            series: [
                {
                    name: seriesName,
                    data: []
                }
            ]
        };
    };
    /**
     * This method creates configuration for s3 constructor
     * @returns {S3.Types.ClientConfiguration} S3 configuration object
     */
    ImagingService.prototype.createS3Configuration = function () {
        return {
            accessKeyId: this.appConstants.buckets.imaging.accessKeyId,
            secretAccessKey: this.appConstants.buckets.imaging.secretAccessKey,
            region: this.appConstants.buckets.imaging.region,
            maxRetries: 0
        };
    };
    Object.defineProperty(ImagingService.prototype, "deleteObjectChunkSize", {
        /**
         * Chunk size for performing delete operation
         */
        get: function () {
            return this.appConstants.AWS_DELETE_OBJECT_CHUNK_SIZE;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * This methods delete files from the s3 bucket
     * @param {S3.ClientConfiguration} configs
     * @param {String} bucketname
     * @param {Array<string>} fileNames
     */
    ImagingService.prototype.deleteFromBucket = function (configs, bucketname, fileNames) {
        var bucket = new aws_sdk_clients_s3__WEBPACK_IMPORTED_MODULE_2__(configs);
        var params = {
            Bucket: bucketname,
            Delete: {
                Objects: fileNames.map(function (filename) { return ({
                    Key: filename.name
                }); })
            }
        };
        var request = bucket.deleteObjects(params);
        return request.promise();
    };
    /**
     * @private
     * Extracts zip file contents
     * @async
     * @param zipFile
     * @returns {Promise<Array<Blob, String>>} A promise that returns extracted files when resolved
     */
    ImagingService.prototype.getZipContents = function (zipFile) {
        var _this = this;
        return this.utilService
            .readFileAsArrayBuffer(zipFile)
            .then(function (zipFileArrayBuffer) {
            var zip = new _this.JSZip();
            return zip.loadAsync(zipFileArrayBuffer);
        })
            .then(function (zipData) {
            return _this.fileContentExtractor(zipData);
        });
    };
    /**
     * @async
     * Get the hash of a file
     * @param {File} file MD5 has will be calculated of this file
     * @returns {Promise<string>} A Promise that returns hash of a file when resolved
     * ```js
     * getIncrementalHash(fileObject)
     *  .then((hash) => {
     *    // consume hash
     *  })
     *  .catch((error) => {
     *   // error occurred
     *  })
     * ```
     */
    ImagingService.prototype.getIncrementalHash = function (file) {
        var currentChunk = 0;
        var blobSlice = File.prototype.slice;
        var chunkSize = this.CHUNK_SIZES;
        var chunks = Math.ceil(file.size / chunkSize);
        var spark = new this.SparkMD5.ArrayBuffer();
        var fileReader = new FileReader();
        var loadNext = function () {
            var start = currentChunk * chunkSize;
            var end = start + chunkSize >= file.size ? file.size : start + chunkSize;
            fileReader.readAsArrayBuffer(blobSlice.call(file, start, end));
        };
        loadNext();
        return new Promise(function (resolve, reject) {
            fileReader.onload = function (e) {
                spark.append(e.target.result);
                currentChunk++;
                if (currentChunk < chunks) {
                    loadNext();
                }
                else {
                    resolve(spark.end());
                }
            };
            fileReader.onerror = function (err) {
                reject(err);
            };
        });
    };
    /**
     * Get the has of an array buffer
     * @param {ArrayBuffer} array Buffer of which MD5 to calculated
     */
    ImagingService.prototype.getHashArrayBuffer = function (arrayBuffer) {
        var spark = new this.SparkMD5.ArrayBuffer();
        spark.append(arrayBuffer);
        return spark.end();
    };
    /**
     * A user can have multiple designations so this method finds the highest designation a user can have
     * by matching against the predefined authorized designation
     * @param {Map<string, number>} roleMap A map containing user designation and their priority level
     * @param {Array<string>} userDesignations Aesignations an user have
     * this function fails when userDesignations is empty
     * @returns {string} Highest designation a user can have
     * ```js
     * // userHighestRole contains user's highest role
     * const userDesignations = ['Doctor', 'Admin'];
     * const roleMap = new Map([['Admin', 1], ['Technician', 2], ['Doctor', 3]]);
     * // userHighestRole will contain Admin
     * const userHighestRole = getUserHighestRole(
         this.roleMap,
         this.userDesignations
      )
     * ```
     */
    ImagingService.prototype.getUserHighestRole = function (roleMap, userDesignations) {
        // it goes by filtering the user designations
        // if user's designation is in authoized designations it is included
        var filteredDesignation = userDesignations.filter(function (designation) {
            return roleMap.has(designation);
        });
        if (filteredDesignation.length) {
            return (filteredDesignation
                // then it converts userDesignations of the form Array<string>
                // to Array<{ designation: string, priority: number}>
                // if priority has lower value if has more priority
                .map(function (designation) { return ({
                designation: designation,
                priority: roleMap.get(designation)
            }); })
                // then it finds the designation with priority with lowest value
                .reduce(function (previous, currValue) {
                if (previous.priority < currValue.priority) {
                    return previous;
                }
                else {
                    return currValue;
                }
            }).designation);
        }
        else {
            return;
        }
    };
    /**
     * This method checks whether a given file is zip file by verifying its signature
     * @param {File} zip A zip file to validate
     * @returns {Promise<boolean>} Promise which returns a boolean value when resolved
     * ```js
     * isValidZipFile(aFileObject)
     *  .then((value) => {
     *    // is a valid zip file
     *  })
     *  .catch((error) => {
     *    // not a valid zip file
     *  })
     * ```
     */
    ImagingService.prototype.isValidZipFile = function (zip) {
        var _this = this;
        var signatureSet = new Set(['504b34', '504b56', '504b78']); // zip file signatures
        var rejectMessage = 'Seems like file which you have selected is not a valid zip file';
        var blob = zip.slice(0, 4); // reading of first four bytes
        return this.utilService
            .readFileAsArrayBuffer(blob)
            .then(function (value) {
            return _this.fileTypeValidator(value, signatureSet, rejectMessage);
        });
    };
    /**
     * This method checks whether a selected file is a jpeg file
     * @returns {Promise<boolean>} Promise which returns a boolean value when resolved
     * @param jpegFile jpeg file
     */
    ImagingService.prototype.isValidJpegFile = function (jpegFile) {
        var _this = this;
        var signatureSet = new Set(['ffd8ffe0', 'ffd8ffe1', 'ffd8ffdB']);
        var blob = jpegFile.slice(0, 4);
        var rejectMessage = 'Seems like the file which you have selected is not a valid jpeg file';
        return this.utilService
            .readFileAsArrayBuffer(blob)
            .then(function (value) {
            return _this.fileTypeValidator(value, signatureSet, rejectMessage);
        });
    };
    /**
     * This method checks wether a selected file is a dicom file
     * @param dicomFile dicom file
     * @returns {Promise<boolean>} Promise which returns a boolean value when resolved
     */
    ImagingService.prototype.isValidDicomFile = function (dicomFile) {
        var _this = this;
        var signatureSet = new Set(['444943']);
        var blob = dicomFile.slice(0, 10);
        var rejectMessage = 'Seems like the file which you have selected is not a valid dicom file';
        return this.utilService
            .readFileAsArrayBuffer(blob)
            .then(function (value) {
            return _this.fileTypeValidator(value, signatureSet, rejectMessage);
        });
    };
    Object.defineProperty(ImagingService.prototype, "imagingBucketName", {
        /**
         * Returns the imaging bucket name
         */
        get: function () {
            return this.appConstants.buckets.imaging.BucketURL;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(ImagingService.prototype, "imagingJpegBucketName", {
        get: function () {
            return this.appConstants.buckets.imaging.BucketURLJpeg;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * @private
     * Extracts the contents of a zip file;
     * Only takes first level files
     * @param zip A zip file to extract
     * @async
     * @returns {Promise<Array<BLob, String>>} A promise that returns extracted files when resolved
     */
    ImagingService.prototype.fileContentExtractor = function (zip) {
        return tslib__WEBPACK_IMPORTED_MODULE_0__["__awaiter"](this, void 0, void 0, function () {
            var files, extractedFiles, filesNames, _i, filesNames_1, fileName, _a, _b, _c;
            return tslib__WEBPACK_IMPORTED_MODULE_0__["__generator"](this, function (_d) {
                switch (_d.label) {
                    case 0:
                        files = zip.files;
                        extractedFiles = [];
                        filesNames = Object.keys(files);
                        _i = 0, filesNames_1 = filesNames;
                        _d.label = 1;
                    case 1:
                        if (!(_i < filesNames_1.length)) return [3 /*break*/, 4];
                        fileName = filesNames_1[_i];
                        _b = (_a = extractedFiles).push;
                        _c = {};
                        return [4 /*yield*/, files[fileName].async('blob')];
                    case 2:
                        _b.apply(_a, [(_c.fileBlob = _d.sent(),
                                _c.fileName = fileName,
                                _c)]);
                        _d.label = 3;
                    case 3:
                        _i++;
                        return [3 /*break*/, 1];
                    case 4: return [2 /*return*/, extractedFiles];
                }
            });
        });
    };
    /**
     * @ignore
     */
    ImagingService.prototype.fileTypeValidator = function (value, signatureSet, rejectMessage) {
        var uint = new Uint8Array(value); // making a 8 byte wide data view
        var bytes = [];
        uint.forEach(function (byte) {
            bytes.push(byte.toString(16)); // converting each byte into hexadecimal number
        });
        var isValidFile = signatureSet.has(bytes.join(''));
        if (isValidFile) {
            return Promise.resolve(true);
        }
        else {
            return Promise.reject(rejectMessage ||
                'Seems like the file which you have selected is not valid file');
        }
    };
    return ImagingService;
}());



/***/ }),

/***/ "./src/app/modules/imaging/services/roles-constants.service.ts":
/*!*********************************************************************!*\
  !*** ./src/app/modules/imaging/services/roles-constants.service.ts ***!
  \*********************************************************************/
/*! exports provided: ROLES, ROLES_TOKEN */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ROLES", function() { return ROLES; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ROLES_TOKEN", function() { return ROLES_TOKEN; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");

var ROLES = new Map([['Admin', 1], ['Technician', 2], ['Doctor', 3]]);
var ROLES_TOKEN = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["InjectionToken"]('ROLES_TOKEN');


/***/ }),

/***/ "./src/app/modules/imaging/services/valid-user-guard.service.ts":
/*!**********************************************************************!*\
  !*** ./src/app/modules/imaging/services/valid-user-guard.service.ts ***!
  \**********************************************************************/
/*! exports provided: ValidUserGuard */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ValidUserGuard", function() { return ValidUserGuard; });
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _app_modules_imaging_services_imaging_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @app/modules/imaging/services/imaging.service */ "./src/app/modules/imaging/services/imaging.service.ts");
/* harmony import */ var _core_services_user_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @core/services/user.service */ "./src/app/core/services/user.service.ts");



var ValidUserGuard = /** @class */ (function () {
    function ValidUserGuard(roles, router, userService, imagingService) {
        this.router = router;
        this.userService = userService;
        this.imagingService = imagingService;
        this.roles = roles;
    }
    ValidUserGuard.prototype.canActivate = function () {
        try {
            var isValid = this.isValidUser();
            if (!isValid) {
                this.router.navigate(['no-access']);
            }
            else {
                return true;
            }
        }
        catch (e) {
            this.router.navigate(['no-access']);
        }
    };
    ValidUserGuard.prototype.isValidUser = function () {
        var user = this.userService.getUser();
        var designationsList = user.designationsList.map(function (_a) {
            var designation = _a.designation;
            return designation;
        });
        var userHighestRole = this.imagingService.getUserHighestRole(this.roles, designationsList);
        return !!userHighestRole;
    };
    return ValidUserGuard;
}());



/***/ }),

/***/ "./src/app/shared/directives/disable-control.directive.ts":
/*!****************************************************************!*\
  !*** ./src/app/shared/directives/disable-control.directive.ts ***!
  \****************************************************************/
/*! exports provided: DisableControlDirective */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DisableControlDirective", function() { return DisableControlDirective; });
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");

var DisableControlDirective = /** @class */ (function () {
    function DisableControlDirective(ngControl) {
        this.ngControl = ngControl;
    }
    Object.defineProperty(DisableControlDirective.prototype, "appDisableControl", {
        set: function (disabledState) {
            var action = disabledState ? 'enable' : 'disable';
            this.ngControl.control[action]();
        },
        enumerable: true,
        configurable: true
    });
    return DisableControlDirective;
}());



/***/ })

}]);
//# sourceMappingURL=default~modules-imaging-imaging-module-ngfactory~modules-optical-store-opticalStore-module-ngfactory.js.map