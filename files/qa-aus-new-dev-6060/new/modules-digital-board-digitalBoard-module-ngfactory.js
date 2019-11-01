(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["modules-digital-board-digitalBoard-module-ngfactory"],{

/***/ "./node_modules/ngx-filter-pipe/esm5/ngx-filter-pipe.js":
/*!**************************************************************!*\
  !*** ./node_modules/ngx-filter-pipe/esm5/ngx-filter-pipe.js ***!
  \**************************************************************/
/*! exports provided: FilterPipeModule, FilterPipe */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FilterPipeModule", function() { return FilterPipeModule; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FilterPipe", function() { return FilterPipe; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");

/**
 * @fileoverview added by tsickle
 * @suppress {checkTypes} checked by tsc
 */
var FilterPipe = /** @class */ (function () {
    function FilterPipe() {
    }
    /**
     * @param {?} value
     * @param {?} key
     * @return {?}
     */
    FilterPipe.isFoundOnWalking = function (value, key) {
        var /** @type {?} */ walker = value;
        var /** @type {?} */ found = false;
        do {
            if (walker.hasOwnProperty(key) || Object.getOwnPropertyDescriptor(walker, key)) {
                found = true;
                break;
            }
        } while (walker = Object.getPrototypeOf(walker));
        return found;
    };
    /**
     * @param {?} value
     * @return {?}
     */
    FilterPipe.isNumber = function (value) {
        return !isNaN(parseInt(value, 10)) && isFinite(value);
    };
    /**
     * Checks function's value if type is function otherwise same value
     * @param {?} value
     * @return {?}
     */
    FilterPipe.getValue = function (value) {
        return typeof value === 'function' ? value() : value;
    };
    /**
     * @param {?} filter
     * @return {?}
     */
    FilterPipe.prototype.filterByString = function (filter) {
        if (filter) {
            filter = filter.toLowerCase();
        }
        return function (value) { return !filter || (value ? ('' + value).toLowerCase().indexOf(filter) !== -1 : false); };
    };
    /**
     * @param {?} filter
     * @return {?}
     */
    FilterPipe.prototype.filterByBoolean = function (filter) {
        return function (value) { return Boolean(value) === filter; };
    };
    /**
     * @param {?} filter
     * @return {?}
     */
    FilterPipe.prototype.filterByObject = function (filter) {
        var _this = this;
        return function (value) {
            for (var /** @type {?} */ key in filter) {
                if (key === '$or') {
                    if (!_this.filterByOr(filter.$or)(FilterPipe.getValue(value))) {
                        return false;
                    }
                    continue;
                }
                if (!value || !FilterPipe.isFoundOnWalking(value, key)) {
                    return false;
                }
                if (!_this.isMatching(filter[key], FilterPipe.getValue(value[key]))) {
                    return false;
                }
            }
            return true;
        };
    };
    /**
     * @param {?} filter
     * @param {?} val
     * @return {?}
     */
    FilterPipe.prototype.isMatching = function (filter, val) {
        switch (typeof filter) {
            case 'boolean':
                return this.filterByBoolean(filter)(val);
            case 'string':
                return this.filterByString(filter)(val);
            case 'object':
                return this.filterByObject(filter)(val);
        }
        return this.filterDefault(filter)(val);
    };
    /**
     * Filter value by $or
     * @param {?} filter
     * @return {?}
     */
    FilterPipe.prototype.filterByOr = function (filter) {
        var _this = this;
        return function (value) {
            var /** @type {?} */ length = filter.length;
            var /** @type {?} */ arrayComparison = function (i) { return value.indexOf(filter[i]) !== -1; };
            var /** @type {?} */ otherComparison = function (i) { return _this.isMatching(filter[i], value); };
            var /** @type {?} */ comparison = Array.isArray(value) ? arrayComparison : otherComparison;
            for (var /** @type {?} */ i = 0; i < length; i++) {
                if (comparison(i)) {
                    return true;
                }
            }
            return false;
        };
    };
    /**
     * Default filterDefault function
     * @param {?} filter
     * @return {?}
     */
    FilterPipe.prototype.filterDefault = function (filter) {
        return function (value) { return filter === undefined || filter == value; };
    };
    /**
     * @param {?} array
     * @param {?} filter
     * @return {?}
     */
    FilterPipe.prototype.transform = function (array, filter) {
        if (!array) {
            return array;
        }
        switch (typeof filter) {
            case 'boolean':
                return array.filter(this.filterByBoolean(filter));
            case 'string':
                if (FilterPipe.isNumber(filter)) {
                    return array.filter(this.filterDefault(filter));
                }
                return array.filter(this.filterByString(filter));
            case 'object':
                return array.filter(this.filterByObject(filter));
            case 'function':
                return array.filter(filter);
        }
        return array.filter(this.filterDefault(filter));
    };
    return FilterPipe;
}());
FilterPipe.decorators = [
    { type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Pipe"], args: [{
                name: 'filterBy',
                pure: false
            },] },
    { type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"] },
];
/** @nocollapse */
FilterPipe.ctorParameters = function () { return []; };
/**
 * @fileoverview added by tsickle
 * @suppress {checkTypes} checked by tsc
 */
var FilterPipeModule = /** @class */ (function () {
    function FilterPipeModule() {
    }
    return FilterPipeModule;
}());
FilterPipeModule.decorators = [
    { type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"], args: [{
                declarations: [FilterPipe],
                providers: [FilterPipe],
                exports: [FilterPipe]
            },] },
];
/** @nocollapse */
FilterPipeModule.ctorParameters = function () { return []; };
/**
 * @fileoverview added by tsickle
 * @suppress {checkTypes} checked by tsc
 */
/**
 * @fileoverview added by tsickle
 * @suppress {checkTypes} checked by tsc
 */
/**
 * @fileoverview added by tsickle
 * @suppress {checkTypes} checked by tsc
 */
/**
 * Generated bundle index. Do not edit.
 */

//# sourceMappingURL=ngx-filter-pipe.js.map


/***/ }),

/***/ "./node_modules/ngx-virtual-scroller/dist/virtual-scroller.ngfactory.js":
/*!******************************************************************************!*\
  !*** ./node_modules/ngx-virtual-scroller/dist/virtual-scroller.ngfactory.js ***!
  \******************************************************************************/
/*! exports provided: VirtualScrollerModuleNgFactory, RenderType_VirtualScrollerComponent, View_VirtualScrollerComponent_0, View_VirtualScrollerComponent_Host_0, VirtualScrollerComponentNgFactory */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VirtualScrollerModuleNgFactory", function() { return VirtualScrollerModuleNgFactory; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RenderType_VirtualScrollerComponent", function() { return RenderType_VirtualScrollerComponent; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "View_VirtualScrollerComponent_0", function() { return View_VirtualScrollerComponent_0; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "View_VirtualScrollerComponent_Host_0", function() { return View_VirtualScrollerComponent_Host_0; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VirtualScrollerComponentNgFactory", function() { return VirtualScrollerComponentNgFactory; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _virtual_scroller__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./virtual-scroller */ "./node_modules/ngx-virtual-scroller/dist/virtual-scroller.js");
/* harmony import */ var _virtual_scroller__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_virtual_scroller__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/**
 * @fileoverview This file was generated by the Angular template compiler. Do not edit.
 *
 * @suppress {suspiciousCode,uselessCode,missingProperties,missingOverride,checkTypes}
 * tslint:disable
 */ 



var VirtualScrollerModuleNgFactory = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵcmf"](_virtual_scroller__WEBPACK_IMPORTED_MODULE_1__["VirtualScrollerModule"], [], function (_l) { return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmod"]([_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](512, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ComponentFactoryResolver"], _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵCodegenComponentFactoryResolver"], [[8, []], [3, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ComponentFactoryResolver"]], _angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModuleRef"]]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](4608, _angular_common__WEBPACK_IMPORTED_MODULE_2__["NgLocalization"], _angular_common__WEBPACK_IMPORTED_MODULE_2__["NgLocaleLocalization"], [_angular_core__WEBPACK_IMPORTED_MODULE_0__["LOCALE_ID"], [2, _angular_common__WEBPACK_IMPORTED_MODULE_2__["ɵangular_packages_common_common_a"]]]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](1073742336, _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"], _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"], []), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](1073742336, _virtual_scroller__WEBPACK_IMPORTED_MODULE_1__["VirtualScrollerModule"], _virtual_scroller__WEBPACK_IMPORTED_MODULE_1__["VirtualScrollerModule"], [])]); });

var styles_VirtualScrollerComponent = ["[_nghost-%COMP%] {\n      position: relative;\n\t  display: block;\n      -webkit-overflow-scrolling: touch;\n    }\n\t\n\t.horizontal.selfScroll[_nghost-%COMP%] {\n      overflow-y: visible;\n      overflow-x: auto;\n\t}\n\t.vertical.selfScroll[_nghost-%COMP%] {\n      overflow-y: auto;\n      overflow-x: visible;\n\t}\n\t\n    .scrollable-content[_ngcontent-%COMP%] {\n      top: 0;\n      left: 0;\n      width: 100%;\n      height: 100%;\n      max-width: 100vw;\n      max-height: 100vh;\n      position: absolute;\n    }\n\n\t.scrollable-content[_ngcontent-%COMP%]     > * {\n\t\tbox-sizing: border-box;\n\t}\n\t\n\t.horizontal[_nghost-%COMP%] {\n\t\twhite-space: nowrap;\n\t}\n\t\n\t.horizontal[_nghost-%COMP%]   .scrollable-content[_ngcontent-%COMP%] {\n\t\tdisplay: flex;\n\t}\n\t\n\t.horizontal[_nghost-%COMP%]   .scrollable-content[_ngcontent-%COMP%]     > * {\n\t\tflex-shrink: 0;\n\t\tflex-grow: 0;\n\t\twhite-space: initial;\n\t}\n\t\n    .total-padding[_ngcontent-%COMP%] {\n      width: 1px;\n      opacity: 0;\n    }\n    \n    .horizontal[_nghost-%COMP%]   .total-padding[_ngcontent-%COMP%] {\n      height: 100%;\n    }"];
var RenderType_VirtualScrollerComponent = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵcrt"]({ encapsulation: 0, styles: styles_VirtualScrollerComponent, data: {} });

function View_VirtualScrollerComponent_0(_l) { return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵvid"](0, [_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵqud"](402653184, 1, { contentElementRef: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵqud"](402653184, 2, { invisiblePaddingElementRef: 0 }), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵeld"](2, 0, [[2, 0], ["invisiblePadding", 1]], null, 0, "div", [["class", "total-padding"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵeld"](3, 0, [[1, 0], ["content", 1]], null, 1, "div", [["class", "scrollable-content"]], null, null, null, null, null)), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵncd"](null, 0)], null, null); }
function View_VirtualScrollerComponent_Host_0(_l) { return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵvid"](0, [(_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵeld"](0, 0, null, null, 3, "virtual-scroller", [], [[2, "horizontal", null], [2, "vertical", null], [2, "selfScroll", null]], null, null, View_VirtualScrollerComponent_0, RenderType_VirtualScrollerComponent)), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵdid"](1, 1032192, null, 2, _virtual_scroller__WEBPACK_IMPORTED_MODULE_1__["VirtualScrollerComponent"], [_angular_core__WEBPACK_IMPORTED_MODULE_0__["ElementRef"], _angular_core__WEBPACK_IMPORTED_MODULE_0__["Renderer2"], _angular_core__WEBPACK_IMPORTED_MODULE_0__["NgZone"], _angular_core__WEBPACK_IMPORTED_MODULE_0__["ChangeDetectorRef"], _angular_core__WEBPACK_IMPORTED_MODULE_0__["PLATFORM_ID"], [2, "virtualScroller.scrollThrottlingTime"], [2, "virtualScroller.scrollDebounceTime"], [2, "virtualScroller.scrollAnimationTime"], [2, "virtualScroller.scrollbarWidth"], [2, "virtualScroller.scrollbarHeight"], [2, "virtualScroller.checkResizeInterval"], [2, "virtualScroller.resizeBypassRefreshThreshold"], [2, "virtualScroller.modifyOverflowStyleOfParentScroll"], [2, "virtualScroller.stripedTable"]], null, null), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵqud"](335544320, 1, { headerElementRef: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵqud"](335544320, 2, { containerElementRef: 0 })], function (_ck, _v) { _ck(_v, 1, 0); }, function (_ck, _v) { var currVal_0 = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵnov"](_v, 1).horizontal; var currVal_1 = !_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵnov"](_v, 1).horizontal; var currVal_2 = !_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵnov"](_v, 1).parentScroll; _ck(_v, 0, 0, currVal_0, currVal_1, currVal_2); }); }
var VirtualScrollerComponentNgFactory = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵccf"]("virtual-scroller,[virtualScroller]", _virtual_scroller__WEBPACK_IMPORTED_MODULE_1__["VirtualScrollerComponent"], View_VirtualScrollerComponent_Host_0, { executeRefreshOutsideAngularZone: "executeRefreshOutsideAngularZone", enableUnequalChildrenSizes: "enableUnequalChildrenSizes", useMarginInsteadOfTranslate: "useMarginInsteadOfTranslate", modifyOverflowStyleOfParentScroll: "modifyOverflowStyleOfParentScroll", stripedTable: "stripedTable", scrollbarWidth: "scrollbarWidth", scrollbarHeight: "scrollbarHeight", childWidth: "childWidth", childHeight: "childHeight", ssrChildWidth: "ssrChildWidth", ssrChildHeight: "ssrChildHeight", ssrViewportWidth: "ssrViewportWidth", ssrViewportHeight: "ssrViewportHeight", bufferAmount: "bufferAmount", scrollAnimationTime: "scrollAnimationTime", resizeBypassRefreshThreshold: "resizeBypassRefreshThreshold", scrollThrottlingTime: "scrollThrottlingTime", scrollDebounceTime: "scrollDebounceTime", checkResizeInterval: "checkResizeInterval", items: "items", compareItems: "compareItems", horizontal: "horizontal", parentScroll: "parentScroll" }, { update: "update", vsUpdate: "vsUpdate", change: "change", vsChange: "vsChange", start: "start", vsStart: "vsStart", end: "end", vsEnd: "vsEnd" }, ["*"]);



/***/ }),

/***/ "./src/app/modules/digital-board/containers/display-board/display-board.component.ngfactory.js":
/*!*****************************************************************************************************!*\
  !*** ./src/app/modules/digital-board/containers/display-board/display-board.component.ngfactory.js ***!
  \*****************************************************************************************************/
/*! exports provided: RenderType_DoctorsDisplayBoardComponent, View_DoctorsDisplayBoardComponent_0, View_DoctorsDisplayBoardComponent_Host_0, DoctorsDisplayBoardComponentNgFactory */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RenderType_DoctorsDisplayBoardComponent", function() { return RenderType_DoctorsDisplayBoardComponent; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "View_DoctorsDisplayBoardComponent_0", function() { return View_DoctorsDisplayBoardComponent_0; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "View_DoctorsDisplayBoardComponent_Host_0", function() { return View_DoctorsDisplayBoardComponent_Host_0; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DoctorsDisplayBoardComponentNgFactory", function() { return DoctorsDisplayBoardComponentNgFactory; });
/* harmony import */ var _display_board_component_scss_shim_ngstyle__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./display-board.component.scss.shim.ngstyle */ "./src/app/modules/digital-board/containers/display-board/display-board.component.scss.shim.ngstyle.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/flex-layout/flex */ "./node_modules/@angular/flex-layout/esm5/flex.es5.js");
/* harmony import */ var _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout/core */ "./node_modules/@angular/flex-layout/esm5/core.es5.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _angular_flex_layout_extended__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/flex-layout/extended */ "./node_modules/@angular/flex-layout/esm5/extended.es5.js");
/* harmony import */ var _angular_platform_browser__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/platform-browser */ "./node_modules/@angular/platform-browser/fesm5/platform-browser.js");
/* harmony import */ var _display_board_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./display-board.component */ "./src/app/modules/digital-board/containers/display-board/display-board.component.ts");
/* harmony import */ var ngx_toastr__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ngx-toastr */ "./node_modules/ngx-toastr/fesm5/ngx-toastr.js");
/* harmony import */ var _core_services_opd_api_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../../../core/services/opd-api.service */ "./src/app/core/services/opd-api.service.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _ngx_translate_core__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @ngx-translate/core */ "./node_modules/@ngx-translate/core/fesm5/ngx-translate-core.js");
/**
 * @fileoverview This file was generated by the Angular template compiler. Do not edit.
 *
 * @suppress {suspiciousCode,uselessCode,missingProperties,missingOverride,checkTypes}
 * tslint:disable
 */ 












var styles_DoctorsDisplayBoardComponent = [_display_board_component_scss_shim_ngstyle__WEBPACK_IMPORTED_MODULE_0__["styles"]];
var RenderType_DoctorsDisplayBoardComponent = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵcrt"]({ encapsulation: 0, styles: styles_DoctorsDisplayBoardComponent, data: { "animation": [{ type: 7, name: "slideDown", definitions: [{ type: 0, name: "void", styles: { type: 6, styles: { height: 0, opacity: 0 }, offset: null }, options: undefined }, { type: 1, expr: ":enter, :leave", animation: [{ type: 4, styles: null, timings: 200 }], options: null }], options: {} }] } });

function View_DoctorsDisplayBoardComponent_1(_l) { return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵvid"](0, [(_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](0, 0, null, null, 35, "li", [], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](1, 0, null, null, 34, "div", [["class", "clearfix card-container__card bg-white"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](2, 0, null, null, 20, "div", [["fxLayout", "row"]], null, null, null, null, null)), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](3, 671744, null, 0, _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_2__["DefaultLayoutDirective"], [_angular_core__WEBPACK_IMPORTED_MODULE_1__["ElementRef"], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_3__["StyleUtils"], [2, _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_2__["LayoutStyleBuilder"]], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_3__["MediaMarshaller"]], { fxLayout: [0, "fxLayout"] }, null), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](4, 0, null, null, 5, "span", [["class", "card-container__doctor-image"], ["fxFlex", "0 0 auto"]], null, null, null, null, null)), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](5, 671744, null, 0, _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_2__["DefaultFlexDirective"], [_angular_core__WEBPACK_IMPORTED_MODULE_1__["ElementRef"], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_3__["StyleUtils"], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_3__["LAYOUT_CONFIG"], _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_2__["FlexStyleBuilder"], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_3__["MediaMarshaller"]], { fxFlex: [0, "fxFlex"] }, null), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](6, 278528, null, 0, _angular_common__WEBPACK_IMPORTED_MODULE_4__["NgStyle"], [_angular_core__WEBPACK_IMPORTED_MODULE_1__["KeyValueDiffers"], _angular_core__WEBPACK_IMPORTED_MODULE_1__["ElementRef"], _angular_core__WEBPACK_IMPORTED_MODULE_1__["Renderer2"]], { ngStyle: [0, "ngStyle"] }, null), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵpod"](7, { "background-image": 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](8, 933888, null, 0, _angular_flex_layout_extended__WEBPACK_IMPORTED_MODULE_5__["DefaultStyleDirective"], [_angular_core__WEBPACK_IMPORTED_MODULE_1__["ElementRef"], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_3__["StyleUtils"], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_3__["MediaMarshaller"], _angular_core__WEBPACK_IMPORTED_MODULE_1__["KeyValueDiffers"], _angular_core__WEBPACK_IMPORTED_MODULE_1__["Renderer2"], _angular_platform_browser__WEBPACK_IMPORTED_MODULE_6__["DomSanitizer"], [6, _angular_common__WEBPACK_IMPORTED_MODULE_4__["NgStyle"]], [2, _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_3__["SERVER_TOKEN"]], _angular_core__WEBPACK_IMPORTED_MODULE_1__["PLATFORM_ID"]], { ngStyle: [0, "ngStyle"] }, null), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵpod"](9, { "background-image": 0 }), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](10, 0, null, null, 12, "span", [["class", "card-container__doctor-desc"], ["fxLayout", "column"], ["fxLayoutAlign", "center start"]], null, null, null, null, null)), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](11, 671744, null, 0, _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_2__["DefaultLayoutDirective"], [_angular_core__WEBPACK_IMPORTED_MODULE_1__["ElementRef"], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_3__["StyleUtils"], [2, _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_2__["LayoutStyleBuilder"]], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_3__["MediaMarshaller"]], { fxLayout: [0, "fxLayout"] }, null), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](12, 671744, null, 0, _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_2__["DefaultLayoutAlignDirective"], [_angular_core__WEBPACK_IMPORTED_MODULE_1__["ElementRef"], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_3__["StyleUtils"], [2, _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_2__["LayoutAlignStyleBuilder"]], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_3__["MediaMarshaller"]], { fxLayoutAlign: [0, "fxLayoutAlign"] }, null), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](13, 0, null, null, 5, "span", [["class", "txt-color-green"], ["fxLayoutAlign", "center center"]], null, null, null, null, null)), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](14, 671744, null, 0, _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_2__["DefaultLayoutAlignDirective"], [_angular_core__WEBPACK_IMPORTED_MODULE_1__["ElementRef"], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_3__["StyleUtils"], [2, _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_2__["LayoutAlignStyleBuilder"]], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_3__["MediaMarshaller"]], { fxLayoutAlign: [0, "fxLayoutAlign"] }, null), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵted"](-1, null, ["ROOM NO - "])), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](16, 0, null, null, 2, "span", [["class", "number-size"], ["fxLayoutAlign", "center center"]], null, null, null, null, null)), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](17, 671744, null, 0, _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_2__["DefaultLayoutAlignDirective"], [_angular_core__WEBPACK_IMPORTED_MODULE_1__["ElementRef"], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_3__["StyleUtils"], [2, _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_2__["LayoutAlignStyleBuilder"]], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_3__["MediaMarshaller"]], { fxLayoutAlign: [0, "fxLayoutAlign"] }, null), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵted"](18, null, ["", " "])), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](19, 0, null, null, 1, "h4", [["class", "txt-color-blue name--ellipsis no-margins"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵted"](20, null, ["", ""])), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](21, 0, null, null, 1, "p", [["class", "name--ellipsis txt-speciality"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵted"](22, null, ["", ""])), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](23, 0, null, null, 12, "div", [["fxLayout", "row"], ["fxLayoutAlign", "space-between"]], null, null, null, null, null)), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](24, 671744, null, 0, _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_2__["DefaultLayoutDirective"], [_angular_core__WEBPACK_IMPORTED_MODULE_1__["ElementRef"], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_3__["StyleUtils"], [2, _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_2__["LayoutStyleBuilder"]], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_3__["MediaMarshaller"]], { fxLayout: [0, "fxLayout"] }, null), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](25, 671744, null, 0, _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_2__["DefaultLayoutAlignDirective"], [_angular_core__WEBPACK_IMPORTED_MODULE_1__["ElementRef"], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_3__["StyleUtils"], [2, _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_2__["LayoutAlignStyleBuilder"]], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_3__["MediaMarshaller"]], { fxLayoutAlign: [0, "fxLayoutAlign"] }, null), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](26, 0, null, null, 4, "span", [["class", "bg-red text-center p-t-10"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](27, 0, null, null, 3, "span", [["class", "txt-color-yellow "]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵted"](-1, null, ["Current "])), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](29, 0, null, null, 1, "h5", [["class", "token-size"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵted"](30, null, ["", ""])), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](31, 0, null, null, 4, "span", [["class", "bg-blue text-center p-t-10"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](32, 0, null, null, 3, "span", [["class", "txt-color-yellow"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵted"](-1, null, ["Next "])), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](34, 0, null, null, 1, "h5", [["class", "token-size"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵted"](35, null, ["", ""]))], function (_ck, _v) { var _co = _v.component; var currVal_0 = "row"; _ck(_v, 3, 0, currVal_0); var currVal_1 = "0 0 auto"; _ck(_v, 5, 0, currVal_1); var currVal_2 = _ck(_v, 7, 0, (("url(" + (_v.context.$implicit.imagePath || _co.fallbackProfileImage)) + ")")); _ck(_v, 6, 0, currVal_2); var currVal_3 = _ck(_v, 9, 0, (("url(" + (_v.context.$implicit.imagePath || _co.fallbackProfileImage)) + ")")); _ck(_v, 8, 0, currVal_3); var currVal_4 = "column"; _ck(_v, 11, 0, currVal_4); var currVal_5 = "center start"; _ck(_v, 12, 0, currVal_5); var currVal_6 = "center center"; _ck(_v, 14, 0, currVal_6); var currVal_7 = "center center"; _ck(_v, 17, 0, currVal_7); var currVal_11 = "row"; _ck(_v, 24, 0, currVal_11); var currVal_12 = "space-between"; _ck(_v, 25, 0, currVal_12); }, function (_ck, _v) { var currVal_8 = (_v.context.$implicit.consultationRoomNo || "N/A"); _ck(_v, 18, 0, currVal_8); var currVal_9 = _v.context.$implicit.doctorName; _ck(_v, 20, 0, currVal_9); var currVal_10 = _v.context.$implicit.doctorSpeciality; _ck(_v, 22, 0, currVal_10); var currVal_13 = _v.context.$implicit.currentTocken; _ck(_v, 30, 0, currVal_13); var currVal_14 = _v.context.$implicit.nextTocken; _ck(_v, 35, 0, currVal_14); }); }
function View_DoctorsDisplayBoardComponent_0(_l) { return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵvid"](0, [(_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](0, 0, null, null, 3, "div", [["class", "col-md-12 no-padding fixed-height"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](1, 0, null, null, 2, "ul", [["class", "card-container clearfix"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵand"](16777216, null, null, 1, null, View_DoctorsDisplayBoardComponent_1)), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](3, 278528, null, 0, _angular_common__WEBPACK_IMPORTED_MODULE_4__["NgForOf"], [_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewContainerRef"], _angular_core__WEBPACK_IMPORTED_MODULE_1__["TemplateRef"], _angular_core__WEBPACK_IMPORTED_MODULE_1__["IterableDiffers"]], { ngForOf: [0, "ngForOf"] }, null)], function (_ck, _v) { var _co = _v.component; var currVal_0 = _co.newDisplayData; _ck(_v, 3, 0, currVal_0); }, null); }
function View_DoctorsDisplayBoardComponent_Host_0(_l) { return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵvid"](0, [(_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](0, 0, null, null, 1, "app-display-board", [], null, null, null, View_DoctorsDisplayBoardComponent_0, RenderType_DoctorsDisplayBoardComponent)), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](1, 245760, null, 0, _display_board_component__WEBPACK_IMPORTED_MODULE_7__["DoctorsDisplayBoardComponent"], [ngx_toastr__WEBPACK_IMPORTED_MODULE_8__["ToastrService"], _core_services_opd_api_service__WEBPACK_IMPORTED_MODULE_9__["OpdApiService"], _angular_router__WEBPACK_IMPORTED_MODULE_10__["ActivatedRoute"], _ngx_translate_core__WEBPACK_IMPORTED_MODULE_11__["TranslateService"]], null, null)], function (_ck, _v) { _ck(_v, 1, 0); }, null); }
var DoctorsDisplayBoardComponentNgFactory = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵccf"]("app-display-board", _display_board_component__WEBPACK_IMPORTED_MODULE_7__["DoctorsDisplayBoardComponent"], View_DoctorsDisplayBoardComponent_Host_0, {}, {}, []);



/***/ }),

/***/ "./src/app/modules/digital-board/containers/display-board/display-board.component.scss.shim.ngstyle.js":
/*!*************************************************************************************************************!*\
  !*** ./src/app/modules/digital-board/containers/display-board/display-board.component.scss.shim.ngstyle.js ***!
  \*************************************************************************************************************/
/*! exports provided: styles */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "styles", function() { return styles; });
/**
 * @fileoverview This file was generated by the Angular template compiler. Do not edit.
 *
 * @suppress {suspiciousCode,uselessCode,missingProperties,missingOverride,checkTypes}
 * tslint:disable
 */ 
var styles = [".card-container[_ngcontent-%COMP%] {\n  padding: 0;\n  list-style-type: none;\n  border-top: 1px solid #dedede; }\n  .card-container__card[_ngcontent-%COMP%] {\n    width: 100%;\n    padding: 10px;\n    border-radius: 5px;\n    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23); }\n  .card-container__doctor-image[_ngcontent-%COMP%] {\n    display: inline-block;\n    width: 50px;\n    height: 50px;\n    border-radius: 50%;\n    border: 3px solid #195651;\n    background-size: cover;\n    background-position: center;\n    margin-right: 5px; }\n  .card-container__doctor-desc[_ngcontent-%COMP%] {\n    max-width: calc(100% - 55px) !important; }\n  li[_ngcontent-%COMP%] {\n  display: inline-block;\n  padding: 10px;\n  margin-left: 15px; }\n  .number-size[_ngcontent-%COMP%] {\n  font-size: 700;\n  font-weight: 700;\n  text-transform: uppercase; }\n  .token-size[_ngcontent-%COMP%] {\n  color: #ffffff;\n  font-weight: 700;\n  font-size: 24px; }\n  .name--ellipsis[_ngcontent-%COMP%] {\n  width: 100%;\n  max-width: 180px;\n  min-width: 180px;\n  white-space: nowrap;\n  text-overflow: ellipsis;\n  overflow: hidden; }\n  .txt-color-green[_ngcontent-%COMP%] {\n  color: #195651;\n  font-size: 12px;\n  font-weight: 700;\n  text-transform: capitalize; }\n  .txt-color-blue[_ngcontent-%COMP%] {\n  color: #3096d8;\n  font-size: 18px;\n  font-weight: 700; }\n  .txt-color-yellow[_ngcontent-%COMP%] {\n  color: #fef500;\n  font-weight: 700;\n  font-size: 14px; }\n  .txt-speciality[_ngcontent-%COMP%] {\n  font-size: 14px;\n  font-weight: 500; }\n  .bg-red[_ngcontent-%COMP%] {\n  background-color: #ef2408;\n  color: #ffffff;\n  min-width: 110px;\n  border-radius: 5px; }\n  .bg-blue[_ngcontent-%COMP%] {\n  background-color: #3096d8;\n  color: #ffffff;\n  min-width: 110px;\n  border-radius: 5px; }\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvbW9kdWxlcy9kaWdpdGFsLWJvYXJkL2NvbnRhaW5lcnMvZGlzcGxheS1ib2FyZC9EOlxcQXBwb29pbnRtZW50XFxkcnVjYXJlLXVpLWFuZ3VsYXI2L3NyY1xcYXBwXFxtb2R1bGVzXFxkaWdpdGFsLWJvYXJkXFxjb250YWluZXJzXFxkaXNwbGF5LWJvYXJkXFxkaXNwbGF5LWJvYXJkLmNvbXBvbmVudC5zY3NzIiwic3JjL2FwcC9tb2R1bGVzL2RpZ2l0YWwtYm9hcmQvY29udGFpbmVycy9kaXNwbGF5LWJvYXJkL0Q6XFxBcHBvb2ludG1lbnRcXGRydWNhcmUtdWktYW5ndWxhcjYvc3JjXFxhc3NldHNcXHNjc3NcXGNvbW1vbl9zdHlsZXNcXF92YXJpYWJsZXMuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFDQTtFQUNFLFVBQVU7RUFDVixxQkFBcUI7RUFDckIsNkJDNkJlLEVBQUE7RUQ1QmY7SUFDRSxXQUFXO0lBQ1gsYUFBYTtJQUNiLGtCQUFrQjtJQUNsQix3RUFBd0UsRUFBQTtFQUUxRTtJQUNFLHFCQUFxQjtJQUNyQixXQUFXO0lBQ1gsWUFBWTtJQUNaLGtCQUFrQjtJQUNsQix5QkNnQmU7SURmZixzQkFBc0I7SUFDdEIsMkJBQTJCO0lBQzNCLGlCQUFpQixFQUFBO0VBRW5CO0lBQ0UsdUNBQXVDLEVBQUE7RUFJM0M7RUFDRSxxQkFBcUI7RUFFckIsYUFBYTtFQUNiLGlCQUFpQixFQUFBO0VBR25CO0VBQ0UsY0MyQm9DO0VEMUJwQyxnQkMwQm9DO0VEekJwQyx5QkFBeUIsRUFBQTtFQUczQjtFQUNFLGNDbENzQztFRG1DdEMsZ0JDb0JvQztFRG5CcEMsZUFBZSxFQUFBO0VBR2pCO0VBQ0UsV0FBVztFQUNYLGdCQUFnQjtFQUNoQixnQkFBZ0I7RUFDaEIsbUJBQW1CO0VBQ25CLHVCQUF1QjtFQUN2QixnQkFBZ0IsRUFBQTtFQUVsQjtFQUNFLGNDdEJpQjtFRHVCakIsZUNIcUM7RURJckMsZ0JDS29DO0VESnBDLDBCQUEwQixFQUFBO0VBRTVCO0VBQ0UsY0MvQm1CO0VEZ0NuQixlQ1pxQztFRGFyQyxnQkNEb0MsRUFBQTtFREd0QztFQUNFLGNDbENvQjtFRG1DcEIsZ0JDTG9DO0VETXBDLGVDaEJxQyxFQUFBO0VEa0J2QztFQUNFLGVDbkJxQztFRG9CckMsZ0JDWm9DLEVBQUE7RURjdEM7RUFDRSx5QkM5Q2lCO0VEK0NqQixjQ3JFc0M7RURzRXRDLGdCQUFlO0VBQ2Ysa0JBQWtCLEVBQUE7RUFFcEI7RUFDRSx5QkNuRG1CO0VEb0RuQixjQzNFc0M7RUQ0RXRDLGdCQUFlO0VBQ2Ysa0JBQWtCLEVBQUEiLCJmaWxlIjoic3JjL2FwcC9tb2R1bGVzL2RpZ2l0YWwtYm9hcmQvY29udGFpbmVycy9kaXNwbGF5LWJvYXJkL2Rpc3BsYXktYm9hcmQuY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyJAaW1wb3J0ICd2YXJpYWJsZXMnO1xyXG4uY2FyZC1jb250YWluZXIge1xyXG4gIHBhZGRpbmc6IDA7XHJcbiAgbGlzdC1zdHlsZS10eXBlOiBub25lO1xyXG4gIGJvcmRlci10b3A6IDFweCBzb2xpZCAkZ3JheS04NztcclxuICAmX19jYXJkIHtcclxuICAgIHdpZHRoOiAxMDAlO1xyXG4gICAgcGFkZGluZzogMTBweDtcclxuICAgIGJvcmRlci1yYWRpdXM6IDVweDtcclxuICAgIGJveC1zaGFkb3c6IDAgM3B4IDZweCByZ2JhKDAsIDAsIDAsIDAuMTYpLCAwIDNweCA2cHggcmdiYSgwLCAwLCAwLCAwLjIzKTtcclxuICB9XHJcbiAgJl9fZG9jdG9yLWltYWdlIHtcclxuICAgIGRpc3BsYXk6IGlubGluZS1ibG9jaztcclxuICAgIHdpZHRoOiA1MHB4O1xyXG4gICAgaGVpZ2h0OiA1MHB4O1xyXG4gICAgYm9yZGVyLXJhZGl1czogNTAlO1xyXG4gICAgYm9yZGVyOiAzcHggc29saWQgJGRlZXAtY3lhbjtcclxuICAgIGJhY2tncm91bmQtc2l6ZTogY292ZXI7XHJcbiAgICBiYWNrZ3JvdW5kLXBvc2l0aW9uOiBjZW50ZXI7XHJcbiAgICBtYXJnaW4tcmlnaHQ6IDVweDtcclxuICB9XHJcbiAgJl9fZG9jdG9yLWRlc2Mge1xyXG4gICAgbWF4LXdpZHRoOiBjYWxjKDEwMCUgLSA1NXB4KSAhaW1wb3J0YW50O1xyXG4gIH1cclxufVxyXG5cclxubGkge1xyXG4gIGRpc3BsYXk6IGlubGluZS1ibG9jaztcclxuICAvLyB3aWR0aDogMjUlO1xyXG4gIHBhZGRpbmc6IDEwcHg7XHJcbiAgbWFyZ2luLWxlZnQ6IDE1cHg7XHJcbn1cclxuXHJcbi5udW1iZXItc2l6ZSB7XHJcbiAgZm9udC1zaXplOiAkZm9udC1ib2xkO1xyXG4gIGZvbnQtd2VpZ2h0OiAkaGVhZGluZ3MtZm9udC13ZWlnaHQ7XHJcbiAgdGV4dC10cmFuc2Zvcm06IHVwcGVyY2FzZTtcclxufVxyXG5cclxuLnRva2VuLXNpemUge1xyXG4gIGNvbG9yOiAkd2hpdGUtY29sb3I7XHJcbiAgZm9udC13ZWlnaHQ6ICRoZWFkaW5ncy1mb250LXdlaWdodDtcclxuICBmb250LXNpemU6IDI0cHg7XHJcbn1cclxuXHJcbi5uYW1lLS1lbGxpcHNpcyB7XHJcbiAgd2lkdGg6IDEwMCU7XHJcbiAgbWF4LXdpZHRoOiAxODBweDtcclxuICBtaW4td2lkdGg6IDE4MHB4O1xyXG4gIHdoaXRlLXNwYWNlOiBub3dyYXA7XHJcbiAgdGV4dC1vdmVyZmxvdzogZWxsaXBzaXM7XHJcbiAgb3ZlcmZsb3c6IGhpZGRlbjtcclxufVxyXG4udHh0LWNvbG9yLWdyZWVuIHtcclxuICBjb2xvcjogJGRlZXAtY3lhbjtcclxuICBmb250LXNpemU6ICRoNC1mb250LXNpemU7XHJcbiAgZm9udC13ZWlnaHQ6ICRoZWFkaW5ncy1mb250LXdlaWdodDtcclxuICB0ZXh0LXRyYW5zZm9ybTogY2FwaXRhbGl6ZTtcclxufVxyXG4udHh0LWNvbG9yLWJsdWUge1xyXG4gIGNvbG9yOiAkYnJpZ2h0LWJsdWU7XHJcbiAgZm9udC1zaXplOiAkaDEtZm9udC1zaXplO1xyXG4gIGZvbnQtd2VpZ2h0OiAkZm9udC1ib2xkO1xyXG59XHJcbi50eHQtY29sb3IteWVsbG93IHtcclxuICBjb2xvcjogJHZpdmlkLXllbGxvdztcclxuICBmb250LXdlaWdodDogJGZvbnQtYm9sZDtcclxuICBmb250LXNpemU6ICRoMy1mb250LXNpemU7XHJcbn1cclxuLnR4dC1zcGVjaWFsaXR5e1xyXG4gIGZvbnQtc2l6ZTogJGgzLWZvbnQtc2l6ZTtcclxuICBmb250LXdlaWdodDogJGZvbnQtcmVndWxhcjtcclxufVxyXG4uYmctcmVkLCB7XHJcbiAgYmFja2dyb3VuZC1jb2xvcjogJHZpdmlkLXJlZDtcclxuICBjb2xvcjogJHdoaXRlLWNvbG9yO1xyXG4gIG1pbi13aWR0aDoxMTBweDtcclxuICBib3JkZXItcmFkaXVzOiA1cHg7XHJcbn1cclxuLmJnLWJsdWUge1xyXG4gIGJhY2tncm91bmQtY29sb3I6ICRicmlnaHQtYmx1ZTtcclxuICBjb2xvcjogJHdoaXRlLWNvbG9yO1xyXG4gIG1pbi13aWR0aDoxMTBweDtcclxuICBib3JkZXItcmFkaXVzOiA1cHg7XHJcbn1cclxuIiwiLy8gY29sb3IgdmFyaWFibGVzXHJcblxyXG4kbGlnaHQtYmx1ZTogICAgICAgICAgICAgICAgICAgICAjNDg5ZWQ2O1xyXG4kZGFyay1ibHVlOiAgICAgICAgICAgICAgICAgICAgICAjMDczMTRiO1xyXG4kZGFyay1ibHVlLXNpZGUtbmF2OiAgICAgICAgICAgICAjMDQxYjI5O1xyXG4kcGFuZWwtYm9yZGVyLWNvbG9yOiAgICAgICAgICAgICAjZTFlMWUxO1xyXG4kd2hpdGUtY29sb3I6ICAgICAgICAgICAgICAgICAgICAjZmZmZmZmO1xyXG4kbGlnaHQtZ3JlZW46ICAgICAgICAgICAgICAgICAgICAjODVlZDdhO1xyXG4kbWVkaXVtLWdyZXktY29tcC1iZzogICAgICAgICAgICAjZjVmNWY1O1xyXG4kbGlnaHQtZ3JleTogICAgICAgICAgICAgICAgICAgICAjZjhmOGY4O1xyXG4kbGlnaHQtZ3JleS1jb21wLWJnOiAgICAgICAgICAgICAjZWJlYmViO1xyXG4kbWVkaXVtLWdyZXk6ICAgICAgICAgICAgICAgICAgICAjNjY2NjY2O1xyXG4kZGFyay1ncmV5OiAgICAgICAgICAgICAgICAgICAgICAjMzMzMzMzO1xyXG4kbGFiZWwtYmx1ZTogICAgICAgICAgICAgICAgICAgICAjMDA2YmJiO1xyXG4kcGFsZS1ibHVlOiAgICAgICAgICAgICAgICAgICAgICAjZTlmOGZiO1xyXG4kdGhpbi1ibHVlOiAgICAgICAgICAgICAgICAgICAgICAjMDNhOGUwO1xyXG4kZm9ybS1pdGVtLWJsdWU6ICAgICAgICAgICAgICAgICAjMWQ1Zjg5O1xyXG4kYnJvd24tZ3JlZW46ICAgICAgICAgICAgICAgICAgICAjMWU2MTcyO1xyXG4kZGVlcC1yZWQ6ICAgICAgICAgICAgICAgICAgICAgICAjZjczZDBjO1xyXG4kYnV0dG9uLXJlZDogICAgICAgICAgICAgICAgICAgICAjY2IxZDA1O1xyXG4kbmlnaHRSaWRlcjogICAgICAgICAgICAgICAgICAgICByZ2IoNTEsIDUxLCA1MSk7XHJcbiRzaWx2ZXJUcmVlOiAgICAgICAgICAgICAgICAgICAgIHJnYig5NCwgMTk0LCAxNDkpO1xyXG4kY3J1c3RhOiAgICAgICAgICAgICAgICAgICAgICAgICByZ2IoMjQ1LCAxMTIsIDk1KTtcclxuJGdhaW5zYm9ybzogICAgICAgICAgICAgICAgICAgICAgI2RkZGRkZDtcclxuJGJvcmRlci1jb2xvcjogICAgICAgICAgICAgICAgICAgI2Q3ZGZlMztcclxuJGxpZ3QtZ3JleS1jYXJkOiAgICAgICAgICAgICAgICAgI2ZhZmFmYTtcclxuXHJcbi8vIHJlY2VudGx5IGFkZGVkXHJcbiR2aXZpZC1yZWQ6ICNlZjI0MDg7XHJcbiRicmlnaHQtYmx1ZTogIzMwOTZkODtcclxuJHZpdmlkLWJsdWU6ICMwMGE4ZGQ7XHJcbiR2aXZpZC15ZWxsb3c6ICNmZWY1MDA7XHJcbiRkZWVwLWN5YW46ICMxOTU2NTE7XHJcbiRncmF5LTg3OiAjZGVkZWRlO1xyXG5cclxuLy8gYm9yZGVyIHZhcmlhYmxlc1xyXG4kcGFuZWwtYm9yZGVyOiAgICAgICAgICAgICAgICAgICAgIDFweCBzb2xpZCAkcGFuZWwtYm9yZGVyLWNvbG9yO1xyXG5cclxuLy8gYmFja2dyb3VuZCB2YXJpYWJsZXNcclxuJGRhcmstYmx1ZS1iZzogICAgICAgICAgICAgICAgICAgICAkZGFyay1ibHVlO1xyXG5cclxuLy8gdGV4dCBjb2xvcnNcclxuJGxpZ2h0LWdyZWVuLXRleHQ6ICAgICAgICAgICAgICAgICAkbGlnaHQtZ3JlZW47XHJcblxyXG4vLyBmb250IGZhbWlseVxyXG4kZm9udC1mYW1pbHktYm9keTogICAgICAgICAgICAgICAgICdNb250c2VycmF0Jywgc2Fucy1zZXJpZiAhaW1wb3J0YW50O1xyXG5cclxuXHJcbi8vIGZvbnQgc2l6ZXMgZm9yIEhlYWRlciBFbGVtZW50c1xyXG4kaDEtZm9udC1zaXplOiAgICAgICAgICAgICAgICAgICAgIDE4cHg7XHJcbiRoMi1mb250LXNpemU6ICAgICAgICAgICAgICAgICAgICAgMTZweDtcclxuJGgzLWZvbnQtc2l6ZTogICAgICAgICAgICAgICAgICAgICAxNHB4O1xyXG4kaDQtZm9udC1zaXplOiAgICAgICAgICAgICAgICAgICAgIDEycHg7XHJcbiRoNS1mb250LXNpemU6ICAgICAgICAgICAgICAgICAgICAgMTFweDtcclxuJGg2LWZvbnQtc2l6ZTogICAgICAgICAgICAgICAgICAgICAxMHB4O1xyXG5cclxuXHJcbi8vIGZvbnQgd2VpZ2h0XHJcbiRmb250LWxpZ2h0OiAgICAgICAgICAgICAgICAgICAgICAgNDAwO1xyXG4kZm9udC1yZWd1bGFyOiAgICAgICAgICAgICAgICAgICAgIDUwMDtcclxuJGZvbnQtc2VtaWJvbGQ6ICAgICAgICAgICAgICAgICAgICA2MDA7XHJcbiRmb250LWJvbGQ6ICAgICAgICAgICAgICAgICAgICAgICAgNzAwO1xyXG4kZm9udC1leHRyYWJvbGQ6ICAgICAgICAgICAgICAgICAgIDkwMDtcclxuXHJcbi8vIGhlYWRpbmdzXHJcbiRoZWFkaW5ncy1mb250LXdlaWdodDogICAgICAgICAgICAgJGZvbnQtYm9sZDtcclxuJGhlYWRpbmdzLWNvbG9yOiAgICAgICAgICAgICAgICAgICAkZGFyay1ibHVlO1xyXG4kaGVhZGluZ3MtbGluZS1oZWlnaHQ6ICAgICAgICAgICAgIDE4cHg7XHJcblxyXG5cclxuLy9MaW5lIEhlaWdodFxyXG5cclxuJGhlYWRpbmdzLWxpbmUtaGVpZ2h0OiAgICAgICAgICAgIDE4cHg7XHJcblxyXG4kc3BhY2VhbW91bnRzOiAgICAgICAgICAgICAgICAgICAgIDAsIDUsIDgsIDEwLCAxNSwgMjAsIDMwO1xyXG4kc2lkZXM6ICAgICAgICAgICAgICAgICAgICAgICAgICAgIGxlZnQsIHRvcCwgYm90dG9tLCByaWdodDtcclxuJGNvbHMtZ3JpZC1zaXplczogICAgICAgICAgICAgICAgICAxLCAyLCAzLCA0LCA1LCA2LCA3LCA4LCA5LCAxMCwgMTEsIDEyO1xyXG5cclxuLy9UZXh0IFRyYW5zZm9ybVxyXG4kdGV4dC11cHBlcmNhc2U6dXBwZXJjYXNlO1xyXG4kdGV4dC1sb3dlcmNhc2U6bG93ZXJjYXNlO1xyXG4kdGV4dC1jYXBpdGFsaXplOmNhcGl0YWxpemU7XHJcblxyXG5cclxuLy8gYm9yZGVyIHJhZGl1c1xyXG5cclxuJHJhZGl1cy1hbW91bnRzOiAgICAgICAgICAgICAgICAgICA1LCAxMCwgMTUsIDIwO1xyXG4kY29tbW9uLXJhZGl1czogICAgICAgICAgICAgICAgICAgIDVweDtcclxuXHJcblxyXG4vLyBib3JkZXJzIHV0aWxpdGllcyB2YXJpYWJsZXNcclxuJGJvcmRlcnM6IChcclxuICB0b3A6ICRwYW5lbC1ib3JkZXIsXHJcbiAgYm90dG9tOiAkcGFuZWwtYm9yZGVyLFxyXG4gIGxlZnQ6ICRwYW5lbC1ib3JkZXIsXHJcbiAgcmlnaHQ6ICRwYW5lbC1ib3JkZXJcclxuKTtcclxuIl19 */"];



/***/ }),

/***/ "./src/app/modules/digital-board/containers/display-board/display-board.component.ts":
/*!*******************************************************************************************!*\
  !*** ./src/app/modules/digital-board/containers/display-board/display-board.component.ts ***!
  \*******************************************************************************************/
/*! exports provided: DoctorsDisplayBoardComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DoctorsDisplayBoardComponent", function() { return DoctorsDisplayBoardComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _core_services__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @core/services */ "./src/app/core/services/index.ts");
/* harmony import */ var ngx_toastr__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ngx-toastr */ "./node_modules/ngx-toastr/fesm5/ngx-toastr.js");
/* harmony import */ var _ngx_translate_core__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @ngx-translate/core */ "./node_modules/@ngx-translate/core/fesm5/ngx-translate-core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var ngx_auto_unsubscribe__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ngx-auto-unsubscribe */ "./node_modules/ngx-auto-unsubscribe/dist/index.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");









var DoctorsDisplayBoardComponent = /** @class */ (function () {
    function DoctorsDisplayBoardComponent(toaster, opdService, activatedRoute, translate) {
        this.toaster = toaster;
        this.opdService = opdService;
        this.activatedRoute = activatedRoute;
        this.translate = translate;
        this.fetchdetails = []; // fetchdetails is the api we are getting the data in a array.
        this.displayList = []; // DisplayList is new array we are inserting into this whatever data came from api.
        this.currentIndex = 0; // We are giving Current index zero.
        this.MAX_LENGTH = 10;
        this.SET_INTERVAL = 30000; // 30000; // We are givivng 30 sec time inteval for consecutive names changing.
        this.API_INTERVAL = 200000000;
        this.newDisplayData = []; // We are inserting the shuffled values into this array.
        translate.use(translate.getBrowserLang() || 'en'); // Taking Default language as english.
        this.sessionData = this.activatedRoute.snapshot.data.userData;
    }
    DoctorsDisplayBoardComponent.prototype.ngOnInit = function () {
        this.fetchData();
    };
    DoctorsDisplayBoardComponent.prototype.Payload = function () {
        var payload = {
            orgId: this.sessionData.orgId,
            orgGrpId: this.sessionData.orgGroupId,
            createdUsrId: this.sessionData.regId
        };
        return payload;
    };
    DoctorsDisplayBoardComponent.prototype.fetchData = function () {
        var _this = this;
        var apiIntervalShared$ = Object(rxjs__WEBPACK_IMPORTED_MODULE_5__["timer"])(0, this.API_INTERVAL)
            .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["concatMap"])(function () {
            return _this.opdService
                .fetchDetailsForDigitalBoard(_this.Payload())
                .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["map"])(function (response) {
                if (response.responseCode === 'E200') {
                    return response.data.map(function (val) {
                        var copiedObject = Object.assign({}, val);
                        var specialties = copiedObject.doctorSpeciality.split(','); // split is for splitting the string
                        copiedObject.doctorSpeciality = specialties.slice(0, 2).join(', ');
                        /**
                         * @param currentTocken
                         * @param nextTocken
                         *  This is for adding 0(zero) before the numerics upto 9 in token for better user experience.
                         */
                        if (copiedObject.nextTocken) {
                            copiedObject.nextTocken = copiedObject.nextTocken.toString().padStart(2, '0');
                        }
                        if (copiedObject.currentTocken) {
                            copiedObject.currentTocken = copiedObject.currentTocken.toString().padStart(2, '0');
                        }
                        return copiedObject;
                    });
                }
                else {
                    return new Error(response.responseCode);
                }
            }));
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["share"])());
        this.apiCallSubscription = apiIntervalShared$
            .subscribe(function (val) {
            _this.displayList = val;
        });
        apiIntervalShared$.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["first"])())
            .subscribe(function () {
            _this.dataSlicer();
        }, function () {
            _this.toaster.error('This operation is unsuccessful');
        });
    };
    DoctorsDisplayBoardComponent.prototype.dataSlicer = function () {
        var _this = this;
        this.slicerSubscription = Object(rxjs__WEBPACK_IMPORTED_MODULE_5__["timer"])(0, this.SET_INTERVAL)
            .subscribe(function () {
            _this.scrolleDoctorsList();
        }, function () {
            _this.toaster.error('This operation is unsuccessful');
        });
    };
    DoctorsDisplayBoardComponent.prototype.scrolleDoctorsList = function () {
        this.newDisplayData = this.displayList.slice(this.currentIndex, this.currentIndex + this.MAX_LENGTH);
        this.currentIndex += this.MAX_LENGTH; // Assigning the max length to current length.
        if (this.currentIndex >= this.displayList.length - 1) {
            this.currentIndex = 0; // we are making current index zero when display list value becomes five each time.
        }
    };
    Object.defineProperty(DoctorsDisplayBoardComponent.prototype, "fallbackProfileImage", {
        get: function () {
            return 'https://s3.ap-south-1.amazonaws.com/dru.assets/images/app/icons/user-male.png';
        },
        enumerable: true,
        configurable: true
    });
    /**
     *@param ngondestroy is for destroying the component and for unsubscribe the observables and,
     * to avoid the memory leaks.
     */
    DoctorsDisplayBoardComponent.prototype.ngOnDestroy = function () { };
    DoctorsDisplayBoardComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(ngx_auto_unsubscribe__WEBPACK_IMPORTED_MODULE_7__["AutoUnsubscribe"])(),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__metadata"]("design:paramtypes", [ngx_toastr__WEBPACK_IMPORTED_MODULE_3__["ToastrService"],
            _core_services__WEBPACK_IMPORTED_MODULE_2__["OpdApiService"],
            _angular_router__WEBPACK_IMPORTED_MODULE_8__["ActivatedRoute"],
            _ngx_translate_core__WEBPACK_IMPORTED_MODULE_4__["TranslateService"]])
    ], DoctorsDisplayBoardComponent);
    return DoctorsDisplayBoardComponent;
}());



/***/ }),

/***/ "./src/app/modules/digital-board/containers/patients-waiting-board/patients-waiting-board.component.ngfactory.js":
/*!***********************************************************************************************************************!*\
  !*** ./src/app/modules/digital-board/containers/patients-waiting-board/patients-waiting-board.component.ngfactory.js ***!
  \***********************************************************************************************************************/
/*! exports provided: RenderType_PatientsWaitingBoardComponent, View_PatientsWaitingBoardComponent_0, View_PatientsWaitingBoardComponent_Host_0, PatientsWaitingBoardComponentNgFactory */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RenderType_PatientsWaitingBoardComponent", function() { return RenderType_PatientsWaitingBoardComponent; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "View_PatientsWaitingBoardComponent_0", function() { return View_PatientsWaitingBoardComponent_0; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "View_PatientsWaitingBoardComponent_Host_0", function() { return View_PatientsWaitingBoardComponent_Host_0; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PatientsWaitingBoardComponentNgFactory", function() { return PatientsWaitingBoardComponentNgFactory; });
/* harmony import */ var _patients_waiting_board_component_scss_shim_ngstyle__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./patients-waiting-board.component.scss.shim.ngstyle */ "./src/app/modules/digital-board/containers/patients-waiting-board/patients-waiting-board.component.scss.shim.ngstyle.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _node_modules_ng_select_ng_select_ng_select_ngfactory__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../../node_modules/@ng-select/ng-select/ng-select.ngfactory */ "./node_modules/@ng-select/ng-select/ng-select.ngfactory.js");
/* harmony import */ var _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ng-select/ng-select */ "./node_modules/@ng-select/ng-select/fesm5/ng-select.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/flex-layout/flex */ "./node_modules/@angular/flex-layout/esm5/flex.es5.js");
/* harmony import */ var _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/flex-layout/core */ "./node_modules/@angular/flex-layout/esm5/core.es5.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _angular_flex_layout_extended__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/flex-layout/extended */ "./node_modules/@angular/flex-layout/esm5/extended.es5.js");
/* harmony import */ var _angular_platform_browser__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/platform-browser */ "./node_modules/@angular/platform-browser/fesm5/platform-browser.js");
/* harmony import */ var _node_modules_ngx_virtual_scroller_dist_virtual_scroller_ngfactory__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../../../../../node_modules/ngx-virtual-scroller/dist/virtual-scroller.ngfactory */ "./node_modules/ngx-virtual-scroller/dist/virtual-scroller.ngfactory.js");
/* harmony import */ var ngx_virtual_scroller_dist_virtual_scroller__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ngx-virtual-scroller/dist/virtual-scroller */ "./node_modules/ngx-virtual-scroller/dist/virtual-scroller.js");
/* harmony import */ var ngx_virtual_scroller_dist_virtual_scroller__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(ngx_virtual_scroller_dist_virtual_scroller__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var _pipes_doctor_filter_pipe__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../../pipes/doctor-filter.pipe */ "./src/app/modules/digital-board/pipes/doctor-filter.pipe.ts");
/* harmony import */ var _core_services_lib_providers__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ../../../../core/services/lib.providers */ "./src/app/core/services/lib.providers.ts");
/* harmony import */ var _patients_waiting_board_component__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./patients-waiting-board.component */ "./src/app/modules/digital-board/containers/patients-waiting-board/patients-waiting-board.component.ts");
/* harmony import */ var ngx_toastr__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ngx-toastr */ "./node_modules/ngx-toastr/fesm5/ngx-toastr.js");
/* harmony import */ var _core_services_opd_api_service__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ../../../../core/services/opd-api.service */ "./src/app/core/services/opd-api.service.ts");
/* harmony import */ var _core_services_utils_service__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! ../../../../core/services/utils.service */ "./src/app/core/services/utils.service.ts");
/* harmony import */ var _core_services_login_api_service__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! ../../../../core/services/login-api.service */ "./src/app/core/services/login-api.service.ts");
/* harmony import */ var _ngx_translate_core__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! @ngx-translate/core */ "./node_modules/@ngx-translate/core/fesm5/ngx-translate-core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/**
 * @fileoverview This file was generated by the Angular template compiler. Do not edit.
 *
 * @suppress {suspiciousCode,uselessCode,missingProperties,missingOverride,checkTypes}
 * tslint:disable
 */ 





















var styles_PatientsWaitingBoardComponent = [_patients_waiting_board_component_scss_shim_ngstyle__WEBPACK_IMPORTED_MODULE_0__["styles"]];
var RenderType_PatientsWaitingBoardComponent = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵcrt"]({ encapsulation: 0, styles: styles_PatientsWaitingBoardComponent, data: { "animation": [{ type: 7, name: "slideDown", definitions: [{ type: 0, name: "void", styles: { type: 6, styles: { height: 0, opacity: 0 }, offset: null }, options: undefined }, { type: 1, expr: ":enter, :leave", animation: [{ type: 4, styles: null, timings: 200 }], options: null }], options: {} }] } });

function View_PatientsWaitingBoardComponent_1(_l) { return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵvid"](0, [(_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](0, 0, null, null, 45, "div", [["class", " border-bottom bg-white"]], [[24, "@slideDown", 0]], null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](1, 0, null, null, 44, "div", [["class", "col d-flex pb-2 pl-2 m-0"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](2, 0, null, null, 21, "div", [["class", "col-md-4 col-sm-4 col-xs-12"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](3, 0, null, null, 1, "label", [], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵted"](-1, null, ["Doctor "])), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](5, 0, null, null, 18, "ng-select", [["bindLabel", "doctorName"], ["bindValue", "empId"], ["class", "custom ng-select"], ["placeholder", "Search For Doctors"], ["role", "listbox"]], [[2, "ng-select-single", null], [2, "ng-select-typeahead", null], [2, "ng-select-multiple", null], [2, "ng-select-taggable", null], [2, "ng-select-searchable", null], [2, "ng-select-clearable", null], [2, "ng-select-opened", null], [2, "ng-select-disabled", null], [2, "ng-select-filtered", null], [2, "ng-untouched", null], [2, "ng-touched", null], [2, "ng-pristine", null], [2, "ng-dirty", null], [2, "ng-valid", null], [2, "ng-invalid", null], [2, "ng-pending", null]], [[null, "add"], [null, "remove"], [null, "clear"], [null, "ngModelChange"], [null, "keydown"]], function (_v, en, $event) { var ad = true; var _co = _v.component; if (("keydown" === en)) {
        var pd_0 = (_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 7).handleKeyDown($event) !== false);
        ad = (pd_0 && ad);
    } if (("add" === en)) {
        var pd_1 = (_co.onDoctorAdd() !== false);
        ad = (pd_1 && ad);
    } if (("remove" === en)) {
        var pd_2 = (_co.onFilterItemRemoved() !== false);
        ad = (pd_2 && ad);
    } if (("clear" === en)) {
        var pd_3 = (_co.onFilterItemRemoved() !== false);
        ad = (pd_3 && ad);
    } if (("ngModelChange" === en)) {
        var pd_4 = ((_co.item.doctorId.$or = $event) !== false);
        ad = (pd_4 && ad);
    } return ad; }, _node_modules_ng_select_ng_select_ng_select_ngfactory__WEBPACK_IMPORTED_MODULE_2__["View_NgSelectComponent_0"], _node_modules_ng_select_ng_select_ng_select_ngfactory__WEBPACK_IMPORTED_MODULE_2__["RenderType_NgSelectComponent"])), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵprd"](4608, null, _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_3__["ɵd"], _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_3__["ɵd"], []), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](7, 4964352, null, 12, _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_3__["NgSelectComponent"], [[8, "custom"], [8, null], [8, null], _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_3__["NgSelectConfig"], _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_3__["SELECTION_MODEL_FACTORY"], _angular_core__WEBPACK_IMPORTED_MODULE_1__["ElementRef"], _angular_core__WEBPACK_IMPORTED_MODULE_1__["ChangeDetectorRef"], _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_3__["ɵr"]], { bindLabel: [0, "bindLabel"], bindValue: [1, "bindValue"], placeholder: [2, "placeholder"], multiple: [3, "multiple"], items: [4, "items"] }, { clearEvent: "clear", addEvent: "add", removeEvent: "remove" }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](335544320, 1, { optionTemplate: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](335544320, 2, { optgroupTemplate: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](335544320, 3, { labelTemplate: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](335544320, 4, { multiLabelTemplate: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](335544320, 5, { headerTemplate: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](335544320, 6, { footerTemplate: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](335544320, 7, { notFoundTemplate: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](335544320, 8, { typeToSearchTemplate: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](335544320, 9, { loadingTextTemplate: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](335544320, 10, { tagTemplate: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](335544320, 11, { loadingSpinnerTemplate: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](603979776, 12, { ngOptions: 1 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵprd"](1024, null, _angular_forms__WEBPACK_IMPORTED_MODULE_4__["NG_VALUE_ACCESSOR"], function (p0_0) { return [p0_0]; }, [_ng_select_ng_select__WEBPACK_IMPORTED_MODULE_3__["NgSelectComponent"]]), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](21, 671744, null, 0, _angular_forms__WEBPACK_IMPORTED_MODULE_4__["NgModel"], [[8, null], [8, null], [8, null], [6, _angular_forms__WEBPACK_IMPORTED_MODULE_4__["NG_VALUE_ACCESSOR"]]], { model: [0, "model"] }, { update: "ngModelChange" }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵprd"](2048, null, _angular_forms__WEBPACK_IMPORTED_MODULE_4__["NgControl"], null, [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["NgModel"]]), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](23, 16384, null, 0, _angular_forms__WEBPACK_IMPORTED_MODULE_4__["NgControlStatus"], [[4, _angular_forms__WEBPACK_IMPORTED_MODULE_4__["NgControl"]]], null, null), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](24, 0, null, null, 21, "div", [["class", "col-md-4 col-sm-4 col-xs-12"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](25, 0, null, null, 1, "label", [], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵted"](-1, null, ["Specialty"])), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](27, 0, null, null, 18, "ng-select", [["bindLabel", "specialityName"], ["bindValue", "specialityName"], ["class", "custom ng-select"], ["placeholder", "Search For speciality"], ["role", "listbox"]], [[2, "ng-select-single", null], [2, "ng-select-typeahead", null], [2, "ng-select-multiple", null], [2, "ng-select-taggable", null], [2, "ng-select-searchable", null], [2, "ng-select-clearable", null], [2, "ng-select-opened", null], [2, "ng-select-disabled", null], [2, "ng-select-filtered", null], [2, "ng-untouched", null], [2, "ng-touched", null], [2, "ng-pristine", null], [2, "ng-dirty", null], [2, "ng-valid", null], [2, "ng-invalid", null], [2, "ng-pending", null]], [[null, "add"], [null, "clear"], [null, "remove"], [null, "ngModelChange"], [null, "keydown"]], function (_v, en, $event) { var ad = true; var _co = _v.component; if (("keydown" === en)) {
        var pd_0 = (_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 29).handleKeyDown($event) !== false);
        ad = (pd_0 && ad);
    } if (("add" === en)) {
        var pd_1 = (_co.onAddSpecialty() !== false);
        ad = (pd_1 && ad);
    } if (("clear" === en)) {
        var pd_2 = (_co.onFilterItemRemoved() !== false);
        ad = (pd_2 && ad);
    } if (("remove" === en)) {
        var pd_3 = (_co.onFilterItemRemoved() !== false);
        ad = (pd_3 && ad);
    } if (("ngModelChange" === en)) {
        var pd_4 = ((_co.item.specialityId.$or = $event) !== false);
        ad = (pd_4 && ad);
    } return ad; }, _node_modules_ng_select_ng_select_ng_select_ngfactory__WEBPACK_IMPORTED_MODULE_2__["View_NgSelectComponent_0"], _node_modules_ng_select_ng_select_ng_select_ngfactory__WEBPACK_IMPORTED_MODULE_2__["RenderType_NgSelectComponent"])), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵprd"](4608, null, _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_3__["ɵd"], _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_3__["ɵd"], []), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](29, 4964352, null, 12, _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_3__["NgSelectComponent"], [[8, "custom"], [8, null], [8, null], _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_3__["NgSelectConfig"], _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_3__["SELECTION_MODEL_FACTORY"], _angular_core__WEBPACK_IMPORTED_MODULE_1__["ElementRef"], _angular_core__WEBPACK_IMPORTED_MODULE_1__["ChangeDetectorRef"], _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_3__["ɵr"]], { bindLabel: [0, "bindLabel"], bindValue: [1, "bindValue"], placeholder: [2, "placeholder"], multiple: [3, "multiple"], items: [4, "items"] }, { clearEvent: "clear", addEvent: "add", removeEvent: "remove" }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](335544320, 13, { optionTemplate: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](335544320, 14, { optgroupTemplate: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](335544320, 15, { labelTemplate: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](335544320, 16, { multiLabelTemplate: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](335544320, 17, { headerTemplate: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](335544320, 18, { footerTemplate: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](335544320, 19, { notFoundTemplate: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](335544320, 20, { typeToSearchTemplate: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](335544320, 21, { loadingTextTemplate: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](335544320, 22, { tagTemplate: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](335544320, 23, { loadingSpinnerTemplate: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](603979776, 24, { ngOptions: 1 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵprd"](1024, null, _angular_forms__WEBPACK_IMPORTED_MODULE_4__["NG_VALUE_ACCESSOR"], function (p0_0) { return [p0_0]; }, [_ng_select_ng_select__WEBPACK_IMPORTED_MODULE_3__["NgSelectComponent"]]), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](43, 671744, null, 0, _angular_forms__WEBPACK_IMPORTED_MODULE_4__["NgModel"], [[8, null], [8, null], [8, null], [6, _angular_forms__WEBPACK_IMPORTED_MODULE_4__["NG_VALUE_ACCESSOR"]]], { model: [0, "model"] }, { update: "ngModelChange" }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵprd"](2048, null, _angular_forms__WEBPACK_IMPORTED_MODULE_4__["NgControl"], null, [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["NgModel"]]), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](45, 16384, null, 0, _angular_forms__WEBPACK_IMPORTED_MODULE_4__["NgControlStatus"], [[4, _angular_forms__WEBPACK_IMPORTED_MODULE_4__["NgControl"]]], null, null)], function (_ck, _v) { var _co = _v.component; var currVal_17 = "doctorName"; var currVal_18 = "empId"; var currVal_19 = "Search For Doctors"; var currVal_20 = true; var currVal_21 = _co.doctorsList; _ck(_v, 7, 0, currVal_17, currVal_18, currVal_19, currVal_20, currVal_21); var currVal_22 = _co.item.doctorId.$or; _ck(_v, 21, 0, currVal_22); var currVal_39 = "specialityName"; var currVal_40 = "specialityName"; var currVal_41 = "Search For speciality"; var currVal_42 = true; var currVal_43 = _co.doctorsSpecialityList; _ck(_v, 29, 0, currVal_39, currVal_40, currVal_41, currVal_42, currVal_43); var currVal_44 = _co.item.specialityId.$or; _ck(_v, 43, 0, currVal_44); }, function (_ck, _v) { var currVal_0 = undefined; _ck(_v, 0, 0, currVal_0); var currVal_1 = !_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 7).multiple; var currVal_2 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 7).typeahead; var currVal_3 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 7).multiple; var currVal_4 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 7).addTag; var currVal_5 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 7).searchable; var currVal_6 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 7).clearable; var currVal_7 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 7).isOpen; var currVal_8 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 7).disabled; var currVal_9 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 7).filtered; var currVal_10 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 23).ngClassUntouched; var currVal_11 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 23).ngClassTouched; var currVal_12 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 23).ngClassPristine; var currVal_13 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 23).ngClassDirty; var currVal_14 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 23).ngClassValid; var currVal_15 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 23).ngClassInvalid; var currVal_16 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 23).ngClassPending; _ck(_v, 5, 1, [currVal_1, currVal_2, currVal_3, currVal_4, currVal_5, currVal_6, currVal_7, currVal_8, currVal_9, currVal_10, currVal_11, currVal_12, currVal_13, currVal_14, currVal_15, currVal_16]); var currVal_23 = !_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 29).multiple; var currVal_24 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 29).typeahead; var currVal_25 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 29).multiple; var currVal_26 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 29).addTag; var currVal_27 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 29).searchable; var currVal_28 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 29).clearable; var currVal_29 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 29).isOpen; var currVal_30 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 29).disabled; var currVal_31 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 29).filtered; var currVal_32 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 45).ngClassUntouched; var currVal_33 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 45).ngClassTouched; var currVal_34 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 45).ngClassPristine; var currVal_35 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 45).ngClassDirty; var currVal_36 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 45).ngClassValid; var currVal_37 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 45).ngClassInvalid; var currVal_38 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 45).ngClassPending; _ck(_v, 27, 1, [currVal_23, currVal_24, currVal_25, currVal_26, currVal_27, currVal_28, currVal_29, currVal_30, currVal_31, currVal_32, currVal_33, currVal_34, currVal_35, currVal_36, currVal_37, currVal_38]); }); }
function View_PatientsWaitingBoardComponent_3(_l) { return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵvid"](0, [(_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](0, 0, null, null, 29, "div", [["class", "clearfix card-container__card"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](1, 0, null, null, 15, "div", [["fxLayout", "row"]], null, null, null, null, null)), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](2, 671744, null, 0, _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_5__["DefaultLayoutDirective"], [_angular_core__WEBPACK_IMPORTED_MODULE_1__["ElementRef"], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_6__["StyleUtils"], [2, _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_5__["LayoutStyleBuilder"]], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_6__["MediaMarshaller"]], { fxLayout: [0, "fxLayout"] }, null), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](3, 0, null, null, 5, "div", [["class", "card-container__doctor-image m-r-xs"], ["fxFlex", "0 0 auto"]], null, null, null, null, null)), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](4, 671744, null, 0, _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_5__["DefaultFlexDirective"], [_angular_core__WEBPACK_IMPORTED_MODULE_1__["ElementRef"], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_6__["StyleUtils"], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_6__["LAYOUT_CONFIG"], _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_5__["FlexStyleBuilder"], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_6__["MediaMarshaller"]], { fxFlex: [0, "fxFlex"] }, null), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](5, 278528, null, 0, _angular_common__WEBPACK_IMPORTED_MODULE_7__["NgStyle"], [_angular_core__WEBPACK_IMPORTED_MODULE_1__["KeyValueDiffers"], _angular_core__WEBPACK_IMPORTED_MODULE_1__["ElementRef"], _angular_core__WEBPACK_IMPORTED_MODULE_1__["Renderer2"]], { ngStyle: [0, "ngStyle"] }, null), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵpod"](6, { "background-image": 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](7, 933888, null, 0, _angular_flex_layout_extended__WEBPACK_IMPORTED_MODULE_8__["DefaultStyleDirective"], [_angular_core__WEBPACK_IMPORTED_MODULE_1__["ElementRef"], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_6__["StyleUtils"], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_6__["MediaMarshaller"], _angular_core__WEBPACK_IMPORTED_MODULE_1__["KeyValueDiffers"], _angular_core__WEBPACK_IMPORTED_MODULE_1__["Renderer2"], _angular_platform_browser__WEBPACK_IMPORTED_MODULE_9__["DomSanitizer"], [6, _angular_common__WEBPACK_IMPORTED_MODULE_7__["NgStyle"]], [2, _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_6__["SERVER_TOKEN"]], _angular_core__WEBPACK_IMPORTED_MODULE_1__["PLATFORM_ID"]], { ngStyle: [0, "ngStyle"] }, null), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵpod"](8, { "background-image": 0 }), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](9, 0, null, null, 7, "div", [["fxFlex", "0 0 calc(100% - 55px)"], ["fxLayout", "column"], ["fxLayoutAlign", "center start"]], null, null, null, null, null)), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](10, 671744, null, 0, _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_5__["DefaultLayoutDirective"], [_angular_core__WEBPACK_IMPORTED_MODULE_1__["ElementRef"], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_6__["StyleUtils"], [2, _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_5__["LayoutStyleBuilder"]], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_6__["MediaMarshaller"]], { fxLayout: [0, "fxLayout"] }, null), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](11, 671744, null, 0, _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_5__["DefaultLayoutAlignDirective"], [_angular_core__WEBPACK_IMPORTED_MODULE_1__["ElementRef"], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_6__["StyleUtils"], [2, _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_5__["LayoutAlignStyleBuilder"]], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_6__["MediaMarshaller"]], { fxLayoutAlign: [0, "fxLayoutAlign"] }, null), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](12, 671744, null, 0, _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_5__["DefaultFlexDirective"], [_angular_core__WEBPACK_IMPORTED_MODULE_1__["ElementRef"], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_6__["StyleUtils"], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_6__["LAYOUT_CONFIG"], _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_5__["FlexStyleBuilder"], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_6__["MediaMarshaller"]], { fxFlex: [0, "fxFlex"] }, null), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](13, 0, null, null, 1, "p", [["class", "txt-color-blue name--ellipsis m-b-0"]], [[8, "title", 0]], null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵted"](14, null, ["", ""])), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](15, 0, null, null, 1, "span", [["class", "name--ellipsis"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵted"](16, null, ["", ""])), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](17, 0, null, null, 12, "div", [], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](18, 0, null, null, 3, "span", [["class", "txt-color-blue"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵted"](-1, null, ["Today Appointments - "])), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](20, 0, null, null, 1, "span", [["class", "txt-color-green no-size"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵted"](21, null, [" ", " "])), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](22, 0, null, null, 1, "h6", [["class", "txt-color-blue"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵted"](-1, null, ["ROOM NO."])), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](24, 0, null, null, 5, "input", [["class", "txt-field-size"], ["type", "text"]], [[2, "ng-untouched", null], [2, "ng-touched", null], [2, "ng-pristine", null], [2, "ng-dirty", null], [2, "ng-valid", null], [2, "ng-invalid", null], [2, "ng-pending", null]], [[null, "ngModelChange"], [null, "input"], [null, "blur"], [null, "compositionstart"], [null, "compositionend"]], function (_v, en, $event) { var ad = true; if (("input" === en)) {
        var pd_0 = (_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 25)._handleInput($event.target.value) !== false);
        ad = (pd_0 && ad);
    } if (("blur" === en)) {
        var pd_1 = (_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 25).onTouched() !== false);
        ad = (pd_1 && ad);
    } if (("compositionstart" === en)) {
        var pd_2 = (_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 25)._compositionStart() !== false);
        ad = (pd_2 && ad);
    } if (("compositionend" === en)) {
        var pd_3 = (_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 25)._compositionEnd($event.target.value) !== false);
        ad = (pd_3 && ad);
    } if (("ngModelChange" === en)) {
        var pd_4 = ((_v.context.$implicit.consultationRoomNo = $event) !== false);
        ad = (pd_4 && ad);
    } return ad; }, null, null)), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](25, 16384, null, 0, _angular_forms__WEBPACK_IMPORTED_MODULE_4__["DefaultValueAccessor"], [_angular_core__WEBPACK_IMPORTED_MODULE_1__["Renderer2"], _angular_core__WEBPACK_IMPORTED_MODULE_1__["ElementRef"], [2, _angular_forms__WEBPACK_IMPORTED_MODULE_4__["COMPOSITION_BUFFER_MODE"]]], null, null), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵprd"](1024, null, _angular_forms__WEBPACK_IMPORTED_MODULE_4__["NG_VALUE_ACCESSOR"], function (p0_0) { return [p0_0]; }, [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["DefaultValueAccessor"]]), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](27, 671744, null, 0, _angular_forms__WEBPACK_IMPORTED_MODULE_4__["NgModel"], [[8, null], [8, null], [8, null], [6, _angular_forms__WEBPACK_IMPORTED_MODULE_4__["NG_VALUE_ACCESSOR"]]], { model: [0, "model"] }, { update: "ngModelChange" }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵprd"](2048, null, _angular_forms__WEBPACK_IMPORTED_MODULE_4__["NgControl"], null, [_angular_forms__WEBPACK_IMPORTED_MODULE_4__["NgModel"]]), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](29, 16384, null, 0, _angular_forms__WEBPACK_IMPORTED_MODULE_4__["NgControlStatus"], [[4, _angular_forms__WEBPACK_IMPORTED_MODULE_4__["NgControl"]]], null, null)], function (_ck, _v) { var _co = _v.component; var currVal_0 = "row"; _ck(_v, 2, 0, currVal_0); var currVal_1 = "0 0 auto"; _ck(_v, 4, 0, currVal_1); var currVal_2 = _ck(_v, 6, 0, (("url(" + (_v.context.$implicit.imagePath || _co.fallbackProfileImage)) + ")")); _ck(_v, 5, 0, currVal_2); var currVal_3 = _ck(_v, 8, 0, (("url(" + (_v.context.$implicit.imagePath || _co.fallbackProfileImage)) + ")")); _ck(_v, 7, 0, currVal_3); var currVal_4 = "column"; _ck(_v, 10, 0, currVal_4); var currVal_5 = "center start"; _ck(_v, 11, 0, currVal_5); var currVal_6 = "0 0 calc(100% - 55px)"; _ck(_v, 12, 0, currVal_6); var currVal_18 = _v.context.$implicit.consultationRoomNo; _ck(_v, 27, 0, currVal_18); }, function (_ck, _v) { var currVal_7 = _v.context.$implicit.doctorNm; _ck(_v, 13, 0, currVal_7); var currVal_8 = _v.context.$implicit.doctorNm; _ck(_v, 14, 0, currVal_8); var currVal_9 = _v.context.$implicit.speciality; _ck(_v, 16, 0, currVal_9); var currVal_10 = _v.context.$implicit.todayAppointments; _ck(_v, 21, 0, currVal_10); var currVal_11 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 29).ngClassUntouched; var currVal_12 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 29).ngClassTouched; var currVal_13 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 29).ngClassPristine; var currVal_14 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 29).ngClassDirty; var currVal_15 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 29).ngClassValid; var currVal_16 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 29).ngClassInvalid; var currVal_17 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 29).ngClassPending; _ck(_v, 24, 0, currVal_11, currVal_12, currVal_13, currVal_14, currVal_15, currVal_16, currVal_17); }); }
function View_PatientsWaitingBoardComponent_2(_l) { return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵvid"](0, [(_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](0, 0, null, null, 7, "div", [["class", "card-container clearfix"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](1, 0, null, null, 6, "virtual-scroller", [], [[2, "horizontal", null], [2, "vertical", null], [2, "selfScroll", null]], null, null, _node_modules_ngx_virtual_scroller_dist_virtual_scroller_ngfactory__WEBPACK_IMPORTED_MODULE_10__["View_VirtualScrollerComponent_0"], _node_modules_ngx_virtual_scroller_dist_virtual_scroller_ngfactory__WEBPACK_IMPORTED_MODULE_10__["RenderType_VirtualScrollerComponent"])), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](2, 1032192, [["scroll", 4]], 2, ngx_virtual_scroller_dist_virtual_scroller__WEBPACK_IMPORTED_MODULE_11__["VirtualScrollerComponent"], [_angular_core__WEBPACK_IMPORTED_MODULE_1__["ElementRef"], _angular_core__WEBPACK_IMPORTED_MODULE_1__["Renderer2"], _angular_core__WEBPACK_IMPORTED_MODULE_1__["NgZone"], _angular_core__WEBPACK_IMPORTED_MODULE_1__["ChangeDetectorRef"], _angular_core__WEBPACK_IMPORTED_MODULE_1__["PLATFORM_ID"], [2, "virtualScroller.scrollThrottlingTime"], [2, "virtualScroller.scrollDebounceTime"], [2, "virtualScroller.scrollAnimationTime"], [2, "virtualScroller.scrollbarWidth"], [2, "virtualScroller.scrollbarHeight"], [2, "virtualScroller.checkResizeInterval"], [2, "virtualScroller.resizeBypassRefreshThreshold"], [2, "virtualScroller.modifyOverflowStyleOfParentScroll"], [2, "virtualScroller.stripedTable"]], { items: [0, "items"] }, null), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](335544320, 25, { headerElementRef: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵqud"](335544320, 26, { containerElementRef: 0 }), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵppd"](5, 2), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵand"](16777216, null, 0, 1, null, View_PatientsWaitingBoardComponent_3)), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](7, 278528, null, 0, _angular_common__WEBPACK_IMPORTED_MODULE_7__["NgForOf"], [_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewContainerRef"], _angular_core__WEBPACK_IMPORTED_MODULE_1__["TemplateRef"], _angular_core__WEBPACK_IMPORTED_MODULE_1__["IterableDiffers"]], { ngForOf: [0, "ngForOf"] }, null)], function (_ck, _v) { var _co = _v.component; var currVal_3 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵunv"](_v, 2, 0, _ck(_v, 5, 0, _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v.parent, 0), _co.doctors, _co.item)); _ck(_v, 2, 0, currVal_3); var currVal_4 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 2).viewPortItems; _ck(_v, 7, 0, currVal_4); }, function (_ck, _v) { var currVal_0 = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 2).horizontal; var currVal_1 = !_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 2).horizontal; var currVal_2 = !_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵnov"](_v, 2).parentScroll; _ck(_v, 1, 0, currVal_0, currVal_1, currVal_2); }); }
function View_PatientsWaitingBoardComponent_0(_l) { return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵvid"](0, [_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵpid"](0, _pipes_doctor_filter_pipe__WEBPACK_IMPORTED_MODULE_12__["DoctorFilterPipe"], [_core_services_lib_providers__WEBPACK_IMPORTED_MODULE_13__["ARRAY_INTERSECTOR"]]), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](1, 0, null, null, 3, "div", [["class", "col-md-12 common-search-bar m-b-20"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](2, 0, null, null, 2, "div", [["class", "col-md-6 page-tittle-text"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](3, 0, null, null, 1, "h1", [["class", "text-uppercase"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵted"](-1, null, ["patient waiting list token display board settings"])), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](5, 0, null, null, 13, "div", [["class", "box-outer-padding row m-0 p-l-10 p-r-10"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](6, 0, null, null, 12, "div", [["class", "box-panel-content bg-white border-all-side col-sm-12"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](7, 0, null, null, 6, "div", [["class", "col-md-12 no-padding"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](8, 0, null, null, 5, "div", [["class", "col-md-12 pb-3 box-section-title"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](9, 0, null, null, 1, "h3", [], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵted"](-1, null, ["PRACTITIONER LIST"])), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](11, 0, null, null, 2, "span", [["class", "pull-right"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](12, 0, null, null, 1, "button", [["class", "cust-filter-toggler-btn"], ["type", "button"]], null, [[null, "click"]], function (_v, en, $event) { var ad = true; var _co = _v.component; if (("click" === en)) {
        var pd_0 = (_co.selectFilter() !== false);
        ad = (pd_0 && ad);
    } return ad; }, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](13, 0, null, null, 0, "i", [["class", "fa fa-filter"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵand"](16777216, null, null, 1, null, View_PatientsWaitingBoardComponent_1)), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](15, 16384, null, 0, _angular_common__WEBPACK_IMPORTED_MODULE_7__["NgIf"], [_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewContainerRef"], _angular_core__WEBPACK_IMPORTED_MODULE_1__["TemplateRef"]], { ngIf: [0, "ngIf"] }, null), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](16, 0, null, null, 2, "div", [["class", "col-md-12 no-padding fixed-height bg-white"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵand"](16777216, null, null, 1, null, View_PatientsWaitingBoardComponent_2)), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](18, 16384, null, 0, _angular_common__WEBPACK_IMPORTED_MODULE_7__["NgIf"], [_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewContainerRef"], _angular_core__WEBPACK_IMPORTED_MODULE_1__["TemplateRef"]], { ngIf: [0, "ngIf"] }, null), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](19, 0, null, null, 9, "div", [["class", "col-sm-12 p-l-r-5 m-t-b-15 form-button-group"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](20, 0, null, null, 8, "ul", [["class", "mt-2"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](21, 0, null, null, 3, "li", [], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](22, 0, null, null, 2, "button", [["class", "btn-app btn-save"], ["form", "resultEntryForm"], ["type", "submit"]], null, [[null, "click"]], function (_v, en, $event) { var ad = true; var _co = _v.component; if (("click" === en)) {
        var pd_0 = (_co.saveDoctorSettings() !== false);
        ad = (pd_0 && ad);
    } return ad; }, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](23, 0, null, null, 0, "i", [["aria-hidden", "true"], ["class", "fas fa-save fa-btn-icon margin-right-5"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵted"](-1, null, [" Save"])), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](25, 0, null, null, 3, "li", [], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](26, 0, null, null, 2, "button", [["class", "btn-app btn-clear"], ["type", "button"]], null, [[null, "click"]], function (_v, en, $event) { var ad = true; var _co = _v.component; if (("click" === en)) {
        var pd_0 = (_co.clearFunction() !== false);
        ad = (pd_0 && ad);
    } return ad; }, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](27, 0, null, null, 0, "i", [["aria-hidden", "true"], ["class", "mdi mdi-reload fa-btn-icon margin-right-5"]], null, null, null, null, null)), (_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵted"](-1, null, ["clear "]))], function (_ck, _v) { var _co = _v.component; var currVal_0 = _co.showFilters; _ck(_v, 15, 0, currVal_0); var currVal_1 = ((_co.doctors == null) ? null : _co.doctors.length); _ck(_v, 18, 0, currVal_1); }, null); }
function View_PatientsWaitingBoardComponent_Host_0(_l) { return _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵvid"](0, [(_l()(), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵeld"](0, 0, null, null, 1, "app-patients-waiting-board", [], null, null, null, View_PatientsWaitingBoardComponent_0, RenderType_PatientsWaitingBoardComponent)), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵdid"](1, 114688, null, 0, _patients_waiting_board_component__WEBPACK_IMPORTED_MODULE_14__["PatientsWaitingBoardComponent"], [ngx_toastr__WEBPACK_IMPORTED_MODULE_15__["ToastrService"], _core_services_opd_api_service__WEBPACK_IMPORTED_MODULE_16__["OpdApiService"], _core_services_utils_service__WEBPACK_IMPORTED_MODULE_17__["UtilService"], _core_services_lib_providers__WEBPACK_IMPORTED_MODULE_13__["CLONEDEEP"], _core_services_login_api_service__WEBPACK_IMPORTED_MODULE_18__["LoginApiService"], _ngx_translate_core__WEBPACK_IMPORTED_MODULE_19__["TranslateService"], _angular_router__WEBPACK_IMPORTED_MODULE_20__["ActivatedRoute"]], null, null)], function (_ck, _v) { _ck(_v, 1, 0); }, null); }
var PatientsWaitingBoardComponentNgFactory = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵccf"]("app-patients-waiting-board", _patients_waiting_board_component__WEBPACK_IMPORTED_MODULE_14__["PatientsWaitingBoardComponent"], View_PatientsWaitingBoardComponent_Host_0, {}, {}, []);



/***/ }),

/***/ "./src/app/modules/digital-board/containers/patients-waiting-board/patients-waiting-board.component.scss.shim.ngstyle.js":
/*!*******************************************************************************************************************************!*\
  !*** ./src/app/modules/digital-board/containers/patients-waiting-board/patients-waiting-board.component.scss.shim.ngstyle.js ***!
  \*******************************************************************************************************************************/
/*! exports provided: styles */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "styles", function() { return styles; });
/**
 * @fileoverview This file was generated by the Angular template compiler. Do not edit.
 *
 * @suppress {suspiciousCode,uselessCode,missingProperties,missingOverride,checkTypes}
 * tslint:disable
 */ 
var styles = [".ng-select.custom[_ngcontent-%COMP%]     input {\n  height: auto; }\n\n.ng-select.custom[_ngcontent-%COMP%]     .ng-placeholder {\n  position: static !important; }\n\n.card-container[_ngcontent-%COMP%] {\n  margin: 0;\n  padding: 0;\n  height: 100%;\n  list-style-type: none; }\n\n.card-container[_ngcontent-%COMP%]   virtual-scroller[_ngcontent-%COMP%] {\n    display: block;\n    height: 100%;\n    width: 100%; }\n\n.card-container__card[_ngcontent-%COMP%] {\n    float: left;\n    width: calc(100% / 6);\n    padding: 5px;\n    border-bottom: 1px solid #dedede; }\n\n.card-container__card[_ngcontent-%COMP%]:last-child {\n      border-right: 1px solid #dedede; }\n\n.card-container__card[_ngcontent-%COMP%]    + .card-container__card[_ngcontent-%COMP%], .card-container__card[_ngcontent-%COMP%]:first-child {\n      border-right: 1px solid #dedede; }\n\n.card-container__doctor-image[_ngcontent-%COMP%] {\n    display: inline-block;\n    width: 50px;\n    height: 50px;\n    border-radius: 50%;\n    border: 3px solid #195651;\n    background-size: cover;\n    background-position: center;\n    margin-right: 5px; }\n\n.input-field-adjustment[_ngcontent-%COMP%] {\n  margin: 12px; }\n\n.txt-color-blue[_ngcontent-%COMP%] {\n  color: #3096d8; }\n\n.name--ellipsis[_ngcontent-%COMP%] {\n  display: block;\n  width: 100%;\n  white-space: nowrap;\n  text-overflow: ellipsis;\n  overflow: hidden; }\n\n.txt-color-green[_ngcontent-%COMP%] {\n  color: #195651;\n  font-weight: 600; }\n\n.no-size[_ngcontent-%COMP%] {\n  font-size: 15px; }\n\n.common-search-bar[_ngcontent-%COMP%]   .page-tittle-text[_ngcontent-%COMP%]   h1[_ngcontent-%COMP%] {\n  font-weight: 700; }\n\n.txt-field-size[_ngcontent-%COMP%] {\n  width: 40%; }\n\n.form-header[_ngcontent-%COMP%] {\n  border-bottom: none;\n  padding: 10px 0px; }\n\n.cust-filter-toggler-btn[_ngcontent-%COMP%] {\n  padding: 2px 6px;\n  border: 1px solid #489ed6;\n  border-radius: 4px;\n  font-size: 0.8rem;\n  background: -webkit-gradient(linear, left top, left bottom, from(#fcfcfc), to(#e9e9e9));\n  background: linear-gradient(to bottom, #fcfcfc, #e9e9e9); }\n\n.cust-filter-toggler-btn[_ngcontent-%COMP%]:active {\n    color: inherit;\n    background: -webkit-gradient(linear, left top, left bottom, from(#e9e9e9), to(#fcfcfc));\n    background: linear-gradient(to bottom, #e9e9e9, #fcfcfc);\n    box-shadow: unset; }\n\n.fixed-height[_ngcontent-%COMP%] {\n  height: 550px;\n  max-height: 550px;\n  overflow: auto; }\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvbW9kdWxlcy9kaWdpdGFsLWJvYXJkL2NvbnRhaW5lcnMvcGF0aWVudHMtd2FpdGluZy1ib2FyZC9EOlxcQXBwb29pbnRtZW50XFxkcnVjYXJlLXVpLWFuZ3VsYXI2L3NyY1xcYXBwXFxtb2R1bGVzXFxkaWdpdGFsLWJvYXJkXFxjb250YWluZXJzXFxwYXRpZW50cy13YWl0aW5nLWJvYXJkXFxwYXRpZW50cy13YWl0aW5nLWJvYXJkLmNvbXBvbmVudC5zY3NzIiwic3JjL2FwcC9tb2R1bGVzL2RpZ2l0YWwtYm9hcmQvY29udGFpbmVycy9wYXRpZW50cy13YWl0aW5nLWJvYXJkL0Q6XFxBcHBvb2ludG1lbnRcXGRydWNhcmUtdWktYW5ndWxhcjYvc3JjXFxhc3NldHNcXHNjc3NcXGNvbW1vbl9zdHlsZXNcXF92YXJpYWJsZXMuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFDQTtFQUVJLFlBQVksRUFBQTs7QUFGaEI7RUFLSSwyQkFBMkIsRUFBQTs7QUFJL0I7RUFDSSxTQUFTO0VBQ1QsVUFBVTtFQUNWLFlBQVk7RUFDWixxQkFBcUIsRUFBQTs7QUFKekI7SUFNTSxjQUFjO0lBQ2QsWUFBWTtJQUNaLFdBQVcsRUFBQTs7QUFFYjtJQUNJLFdBQVc7SUFDWCxxQkFBb0I7SUFDcEIsWUFBVztJQUNYLGdDQ1NTLEVBQUE7O0FEYlo7TUFLZ0IsK0JDUUosRUFBQTs7QURiWjtNQU13QiwrQkNPWixFQUFBOztBRExiO0lBQ0kscUJBQXFCO0lBQ3JCLFdBQVU7SUFDVixZQUFXO0lBQ1gsa0JBQWlCO0lBQ2pCLHlCQ0RXO0lERVgsc0JBQXNCO0lBQ3RCLDJCQUEyQjtJQUMzQixpQkFBaUIsRUFBQTs7QUFHekI7RUFDSSxZQUFXLEVBQUE7O0FBRWY7RUFDSSxjQ2RpQixFQUFBOztBRGdCckI7RUFDSSxjQUFjO0VBQ2QsV0FBVztFQUNYLG1CQUFtQjtFQUNuQix1QkFBdUI7RUFDdkIsZ0JBQWdCLEVBQUE7O0FBRXBCO0VBQ0ksY0NyQmU7RURzQmYsZ0JDTWtDLEVBQUE7O0FESHRDO0VBQ0ksZUFBYyxFQUFBOztBQUdsQjtFQUNJLGdCQ0RrQyxFQUFBOztBREl0QztFQUNJLFVBQVMsRUFBQTs7QUFFYjtFQUNFLG1CQUFtQjtFQUNuQixpQkFBaUIsRUFBQTs7QUFJbkI7RUFDRSxnQkFBZ0I7RUFDaEIseUJDMUVzQztFRDJFdEMsa0JBQWtCO0VBQ2xCLGlCQUFpQjtFQUNqQix1RkFJQztFQUpELHdEQUlDLEVBQUE7O0FBVEg7SUFXSSxjQUFjO0lBQ2QsdUZBSUM7SUFKRCx3REFJQztJQUNELGlCQUFpQixFQUFBOztBQUlyQjtFQUNFLGFBQWE7RUFDYixpQkFBaUI7RUFDakIsY0FBYSxFQUFBIiwiZmlsZSI6InNyYy9hcHAvbW9kdWxlcy9kaWdpdGFsLWJvYXJkL2NvbnRhaW5lcnMvcGF0aWVudHMtd2FpdGluZy1ib2FyZC9wYXRpZW50cy13YWl0aW5nLWJvYXJkLmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiQGltcG9ydCAndmFyaWFibGVzJztcclxuLm5nLXNlbGVjdC5jdXN0b20gOjpuZy1kZWVwIHtcclxuICBpbnB1dCB7XHJcbiAgICBoZWlnaHQ6IGF1dG87XHJcbiAgfVxyXG4gIC5uZy1wbGFjZWhvbGRlciB7XHJcbiAgICBwb3NpdGlvbjogc3RhdGljICFpbXBvcnRhbnQ7XHJcbiAgfVxyXG59XHJcblxyXG4uY2FyZC1jb250YWluZXIge1xyXG4gICAgbWFyZ2luOiAwO1xyXG4gICAgcGFkZGluZzogMDtcclxuICAgIGhlaWdodDogMTAwJTtcclxuICAgIGxpc3Qtc3R5bGUtdHlwZTogbm9uZTtcclxuICAgIHZpcnR1YWwtc2Nyb2xsZXIge1xyXG4gICAgICBkaXNwbGF5OiBibG9jaztcclxuICAgICAgaGVpZ2h0OiAxMDAlO1xyXG4gICAgICB3aWR0aDogMTAwJTtcclxuICAgIH1cclxuICAgICZfX2NhcmQge1xyXG4gICAgICAgIGZsb2F0OiBsZWZ0O1xyXG4gICAgICAgIHdpZHRoOmNhbGMoMTAwJSAvIDYpO1xyXG4gICAgICAgIHBhZGRpbmc6NXB4O1xyXG4gICAgICAgIGJvcmRlci1ib3R0b206IDFweCBzb2xpZCAkZ3JheS04NztcclxuICAgICAgJjpsYXN0LWNoaWxkIHsgYm9yZGVyLXJpZ2h0OiAxcHggc29saWQgJGdyYXktODc7IH1cclxuICAgICAgJiArICYsICY6Zmlyc3QtY2hpbGQgeyBib3JkZXItcmlnaHQ6IDFweCBzb2xpZCAkZ3JheS04NzsgfVxyXG4gICAgfVxyXG4gICAgJl9fZG9jdG9yLWltYWdlIHtcclxuICAgICAgICBkaXNwbGF5OiBpbmxpbmUtYmxvY2s7XHJcbiAgICAgICAgd2lkdGg6NTBweDtcclxuICAgICAgICBoZWlnaHQ6NTBweDtcclxuICAgICAgICBib3JkZXItcmFkaXVzOjUwJTtcclxuICAgICAgICBib3JkZXI6M3B4IHNvbGlkICRkZWVwLWN5YW47XHJcbiAgICAgICAgYmFja2dyb3VuZC1zaXplOiBjb3ZlcjtcclxuICAgICAgICBiYWNrZ3JvdW5kLXBvc2l0aW9uOiBjZW50ZXI7XHJcbiAgICAgICAgbWFyZ2luLXJpZ2h0OiA1cHg7XHJcbiAgICB9XHJcbn1cclxuLmlucHV0LWZpZWxkLWFkanVzdG1lbnR7XHJcbiAgICBtYXJnaW46MTJweDtcclxufVxyXG4udHh0LWNvbG9yLWJsdWV7XHJcbiAgICBjb2xvcjogJGJyaWdodC1ibHVlO1xyXG59XHJcbi5uYW1lLS1lbGxpcHNpc3tcclxuICAgIGRpc3BsYXk6IGJsb2NrO1xyXG4gICAgd2lkdGg6IDEwMCU7XHJcbiAgICB3aGl0ZS1zcGFjZTogbm93cmFwO1xyXG4gICAgdGV4dC1vdmVyZmxvdzogZWxsaXBzaXM7XHJcbiAgICBvdmVyZmxvdzogaGlkZGVuO1xyXG59XHJcbi50eHQtY29sb3ItZ3JlZW57XHJcbiAgICBjb2xvcjokZGVlcC1jeWFuO1xyXG4gICAgZm9udC13ZWlnaHQ6ICRmb250LXNlbWlib2xkO1xyXG59XHJcblxyXG4ubm8tc2l6ZXtcclxuICAgIGZvbnQtc2l6ZToxNXB4O1xyXG59XHJcblxyXG4uY29tbW9uLXNlYXJjaC1iYXIgLnBhZ2UtdGl0dGxlLXRleHQgaDEge1xyXG4gICAgZm9udC13ZWlnaHQ6ICRmb250LWJvbGQ7XHJcbn1cclxuXHJcbi50eHQtZmllbGQtc2l6ZXtcclxuICAgIHdpZHRoOjQwJTtcclxufVxyXG4uZm9ybS1oZWFkZXIge1xyXG4gIGJvcmRlci1ib3R0b206IG5vbmU7XHJcbiAgcGFkZGluZzogMTBweCAwcHg7XHJcbn1cclxuXHJcblxyXG4uY3VzdC1maWx0ZXItdG9nZ2xlci1idG4ge1xyXG4gIHBhZGRpbmc6IDJweCA2cHg7XHJcbiAgYm9yZGVyOiAxcHggc29saWQgJGxpZ2h0LWJsdWU7XHJcbiAgYm9yZGVyLXJhZGl1czogNHB4O1xyXG4gIGZvbnQtc2l6ZTogMC44cmVtO1xyXG4gIGJhY2tncm91bmQ6IGxpbmVhci1ncmFkaWVudChcclxuICAgIHRvIGJvdHRvbSxcclxuICAgIHJnYigyNTIsIDI1MiwgMjUyKSxcclxuICAgIHJnYigyMzMsIDIzMywgMjMzKVxyXG4gICk7XHJcbiAgJjphY3RpdmUge1xyXG4gICAgY29sb3I6IGluaGVyaXQ7XHJcbiAgICBiYWNrZ3JvdW5kOiBsaW5lYXItZ3JhZGllbnQoXHJcbiAgICAgIHRvIGJvdHRvbSxcclxuICAgICAgcmdiKDIzMywgMjMzLCAyMzMpLFxyXG4gICAgICByZ2IoMjUyLCAyNTIsIDI1MilcclxuICAgICk7XHJcbiAgICBib3gtc2hhZG93OiB1bnNldDtcclxuICB9XHJcbn1cclxuXHJcbi5maXhlZC1oZWlnaHQge1xyXG4gIGhlaWdodDogNTUwcHg7XHJcbiAgbWF4LWhlaWdodDogNTUwcHg7XHJcbiAgb3ZlcmZsb3c6YXV0bztcclxufVxyXG5cclxuIiwiLy8gY29sb3IgdmFyaWFibGVzXHJcblxyXG4kbGlnaHQtYmx1ZTogICAgICAgICAgICAgICAgICAgICAjNDg5ZWQ2O1xyXG4kZGFyay1ibHVlOiAgICAgICAgICAgICAgICAgICAgICAjMDczMTRiO1xyXG4kZGFyay1ibHVlLXNpZGUtbmF2OiAgICAgICAgICAgICAjMDQxYjI5O1xyXG4kcGFuZWwtYm9yZGVyLWNvbG9yOiAgICAgICAgICAgICAjZTFlMWUxO1xyXG4kd2hpdGUtY29sb3I6ICAgICAgICAgICAgICAgICAgICAjZmZmZmZmO1xyXG4kbGlnaHQtZ3JlZW46ICAgICAgICAgICAgICAgICAgICAjODVlZDdhO1xyXG4kbWVkaXVtLWdyZXktY29tcC1iZzogICAgICAgICAgICAjZjVmNWY1O1xyXG4kbGlnaHQtZ3JleTogICAgICAgICAgICAgICAgICAgICAjZjhmOGY4O1xyXG4kbGlnaHQtZ3JleS1jb21wLWJnOiAgICAgICAgICAgICAjZWJlYmViO1xyXG4kbWVkaXVtLWdyZXk6ICAgICAgICAgICAgICAgICAgICAjNjY2NjY2O1xyXG4kZGFyay1ncmV5OiAgICAgICAgICAgICAgICAgICAgICAjMzMzMzMzO1xyXG4kbGFiZWwtYmx1ZTogICAgICAgICAgICAgICAgICAgICAjMDA2YmJiO1xyXG4kcGFsZS1ibHVlOiAgICAgICAgICAgICAgICAgICAgICAjZTlmOGZiO1xyXG4kdGhpbi1ibHVlOiAgICAgICAgICAgICAgICAgICAgICAjMDNhOGUwO1xyXG4kZm9ybS1pdGVtLWJsdWU6ICAgICAgICAgICAgICAgICAjMWQ1Zjg5O1xyXG4kYnJvd24tZ3JlZW46ICAgICAgICAgICAgICAgICAgICAjMWU2MTcyO1xyXG4kZGVlcC1yZWQ6ICAgICAgICAgICAgICAgICAgICAgICAjZjczZDBjO1xyXG4kYnV0dG9uLXJlZDogICAgICAgICAgICAgICAgICAgICAjY2IxZDA1O1xyXG4kbmlnaHRSaWRlcjogICAgICAgICAgICAgICAgICAgICByZ2IoNTEsIDUxLCA1MSk7XHJcbiRzaWx2ZXJUcmVlOiAgICAgICAgICAgICAgICAgICAgIHJnYig5NCwgMTk0LCAxNDkpO1xyXG4kY3J1c3RhOiAgICAgICAgICAgICAgICAgICAgICAgICByZ2IoMjQ1LCAxMTIsIDk1KTtcclxuJGdhaW5zYm9ybzogICAgICAgICAgICAgICAgICAgICAgI2RkZGRkZDtcclxuJGJvcmRlci1jb2xvcjogICAgICAgICAgICAgICAgICAgI2Q3ZGZlMztcclxuJGxpZ3QtZ3JleS1jYXJkOiAgICAgICAgICAgICAgICAgI2ZhZmFmYTtcclxuXHJcbi8vIHJlY2VudGx5IGFkZGVkXHJcbiR2aXZpZC1yZWQ6ICNlZjI0MDg7XHJcbiRicmlnaHQtYmx1ZTogIzMwOTZkODtcclxuJHZpdmlkLWJsdWU6ICMwMGE4ZGQ7XHJcbiR2aXZpZC15ZWxsb3c6ICNmZWY1MDA7XHJcbiRkZWVwLWN5YW46ICMxOTU2NTE7XHJcbiRncmF5LTg3OiAjZGVkZWRlO1xyXG5cclxuLy8gYm9yZGVyIHZhcmlhYmxlc1xyXG4kcGFuZWwtYm9yZGVyOiAgICAgICAgICAgICAgICAgICAgIDFweCBzb2xpZCAkcGFuZWwtYm9yZGVyLWNvbG9yO1xyXG5cclxuLy8gYmFja2dyb3VuZCB2YXJpYWJsZXNcclxuJGRhcmstYmx1ZS1iZzogICAgICAgICAgICAgICAgICAgICAkZGFyay1ibHVlO1xyXG5cclxuLy8gdGV4dCBjb2xvcnNcclxuJGxpZ2h0LWdyZWVuLXRleHQ6ICAgICAgICAgICAgICAgICAkbGlnaHQtZ3JlZW47XHJcblxyXG4vLyBmb250IGZhbWlseVxyXG4kZm9udC1mYW1pbHktYm9keTogICAgICAgICAgICAgICAgICdNb250c2VycmF0Jywgc2Fucy1zZXJpZiAhaW1wb3J0YW50O1xyXG5cclxuXHJcbi8vIGZvbnQgc2l6ZXMgZm9yIEhlYWRlciBFbGVtZW50c1xyXG4kaDEtZm9udC1zaXplOiAgICAgICAgICAgICAgICAgICAgIDE4cHg7XHJcbiRoMi1mb250LXNpemU6ICAgICAgICAgICAgICAgICAgICAgMTZweDtcclxuJGgzLWZvbnQtc2l6ZTogICAgICAgICAgICAgICAgICAgICAxNHB4O1xyXG4kaDQtZm9udC1zaXplOiAgICAgICAgICAgICAgICAgICAgIDEycHg7XHJcbiRoNS1mb250LXNpemU6ICAgICAgICAgICAgICAgICAgICAgMTFweDtcclxuJGg2LWZvbnQtc2l6ZTogICAgICAgICAgICAgICAgICAgICAxMHB4O1xyXG5cclxuXHJcbi8vIGZvbnQgd2VpZ2h0XHJcbiRmb250LWxpZ2h0OiAgICAgICAgICAgICAgICAgICAgICAgNDAwO1xyXG4kZm9udC1yZWd1bGFyOiAgICAgICAgICAgICAgICAgICAgIDUwMDtcclxuJGZvbnQtc2VtaWJvbGQ6ICAgICAgICAgICAgICAgICAgICA2MDA7XHJcbiRmb250LWJvbGQ6ICAgICAgICAgICAgICAgICAgICAgICAgNzAwO1xyXG4kZm9udC1leHRyYWJvbGQ6ICAgICAgICAgICAgICAgICAgIDkwMDtcclxuXHJcbi8vIGhlYWRpbmdzXHJcbiRoZWFkaW5ncy1mb250LXdlaWdodDogICAgICAgICAgICAgJGZvbnQtYm9sZDtcclxuJGhlYWRpbmdzLWNvbG9yOiAgICAgICAgICAgICAgICAgICAkZGFyay1ibHVlO1xyXG4kaGVhZGluZ3MtbGluZS1oZWlnaHQ6ICAgICAgICAgICAgIDE4cHg7XHJcblxyXG5cclxuLy9MaW5lIEhlaWdodFxyXG5cclxuJGhlYWRpbmdzLWxpbmUtaGVpZ2h0OiAgICAgICAgICAgIDE4cHg7XHJcblxyXG4kc3BhY2VhbW91bnRzOiAgICAgICAgICAgICAgICAgICAgIDAsIDUsIDgsIDEwLCAxNSwgMjAsIDMwO1xyXG4kc2lkZXM6ICAgICAgICAgICAgICAgICAgICAgICAgICAgIGxlZnQsIHRvcCwgYm90dG9tLCByaWdodDtcclxuJGNvbHMtZ3JpZC1zaXplczogICAgICAgICAgICAgICAgICAxLCAyLCAzLCA0LCA1LCA2LCA3LCA4LCA5LCAxMCwgMTEsIDEyO1xyXG5cclxuLy9UZXh0IFRyYW5zZm9ybVxyXG4kdGV4dC11cHBlcmNhc2U6dXBwZXJjYXNlO1xyXG4kdGV4dC1sb3dlcmNhc2U6bG93ZXJjYXNlO1xyXG4kdGV4dC1jYXBpdGFsaXplOmNhcGl0YWxpemU7XHJcblxyXG5cclxuLy8gYm9yZGVyIHJhZGl1c1xyXG5cclxuJHJhZGl1cy1hbW91bnRzOiAgICAgICAgICAgICAgICAgICA1LCAxMCwgMTUsIDIwO1xyXG4kY29tbW9uLXJhZGl1czogICAgICAgICAgICAgICAgICAgIDVweDtcclxuXHJcblxyXG4vLyBib3JkZXJzIHV0aWxpdGllcyB2YXJpYWJsZXNcclxuJGJvcmRlcnM6IChcclxuICB0b3A6ICRwYW5lbC1ib3JkZXIsXHJcbiAgYm90dG9tOiAkcGFuZWwtYm9yZGVyLFxyXG4gIGxlZnQ6ICRwYW5lbC1ib3JkZXIsXHJcbiAgcmlnaHQ6ICRwYW5lbC1ib3JkZXJcclxuKTtcclxuIl19 */"];



/***/ }),

/***/ "./src/app/modules/digital-board/containers/patients-waiting-board/patients-waiting-board.component.ts":
/*!*************************************************************************************************************!*\
  !*** ./src/app/modules/digital-board/containers/patients-waiting-board/patients-waiting-board.component.ts ***!
  \*************************************************************************************************************/
/*! exports provided: PatientsWaitingBoardComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PatientsWaitingBoardComponent", function() { return PatientsWaitingBoardComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var ngx_toastr__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ngx-toastr */ "./node_modules/ngx-toastr/fesm5/ngx-toastr.js");
/* harmony import */ var _core_services__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @core/services */ "./src/app/core/services/index.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var _ngx_translate_core__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @ngx-translate/core */ "./node_modules/@ngx-translate/core/fesm5/ngx-translate-core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");






var PatientsWaitingBoardComponent = /** @class */ (function () {
    function PatientsWaitingBoardComponent(toaster, opdService, utilService, cloner, loginApiService, translate, activatedRoute) {
        this.toaster = toaster;
        this.opdService = opdService;
        this.utilService = utilService;
        this.cloner = cloner;
        this.loginApiService = loginApiService;
        this.translate = translate;
        this.fetchdetails = [];
        this.doctorsSpecialityList = [];
        this.doctorsList = [];
        this.item = {
            doctorId: {},
            specialityId: {}
        };
        this.showFilters = false; // showfilters is for showing and hiding the search elements.
        translate.use(translate.getBrowserLang() || 'en'); // translate is for converting the languge into required lang,
        this.sessionData = activatedRoute.snapshot.data.userData;
    }
    PatientsWaitingBoardComponent.prototype.ngOnInit = function () {
        this.fetchDoctorSettings();
        this.getEmpListBasedOnDesignation();
        this.fetchListOfSpecialities();
    };
    PatientsWaitingBoardComponent.prototype.getCommonPayload = function () {
        var payload = {
            orgId: this.sessionData.orgId,
            orgGrpId: this.sessionData.orgGroupId,
            createdUsrId: this.sessionData.regId
        };
        return payload;
    };
    PatientsWaitingBoardComponent.prototype.onAddSpecialty = function () {
        this.item = this.cloner(this.item);
    };
    PatientsWaitingBoardComponent.prototype.onDoctorAdd = function () {
        this.item = this.cloner(this.item);
    };
    PatientsWaitingBoardComponent.prototype.onFilterItemRemoved = function () {
        var itemclone = this.cloner(this.item);
        if (itemclone.doctorId.$or && !itemclone.doctorId.$or.length) {
            delete itemclone.doctorId.$or;
        }
        if (itemclone.specialityId.$or && !itemclone.specialityId.$or.length) {
            delete itemclone.specialityId.$or;
        }
        this.item = itemclone;
    };
    PatientsWaitingBoardComponent.prototype.getCommonPayload2 = function () {
        var payload = {
            orgId: this.sessionData.orgId,
            orgGroupId: this.sessionData.orgGroupId,
            authenticatedUserId: this.sessionData.regId,
            regId: this.sessionData.regId,
            designation: 'Doctor',
            orgGrpId: this.sessionData.orgGroupId,
        };
        return payload;
    };
    PatientsWaitingBoardComponent.prototype.makeHiddenProperty = function (obj, property) {
        Object.defineProperty(obj, property, {
            enumerable: false,
            writable: true,
            configurable: false // And returning that value to the database for storing.
        });
    };
    PatientsWaitingBoardComponent.prototype.saveDoctorSettings = function () {
        // this.filterFunction();
        this.insertDoctorSettings();
        // this.updateDoctorSettings();s
    };
    /**
     * In this fetchdoctorSettings function we are calling an api
     * and in that api we are recieving the avoilable doctors list while loading the browser.
     */
    PatientsWaitingBoardComponent.prototype.fetchDoctorSettings = function () {
        var _this = this;
        this.opdService
            .fetchDoctorSettings(this.getCommonPayload())
            .subscribe(function (response) {
            if (response.responseCode === 'E200') {
                _this.doctors = response.data;
                _this.doctors.forEach(function (val, index) {
                    _this.makeHiddenProperty(val, 'consultationRoomNo$$');
                    _this.makeHiddenProperty(val, '_id');
                    if (val.consultationRoomNo === undefined ||
                        val.consultationRoomNo === null) {
                        val.consultationRoomNo = '';
                    }
                    val.consultationRoomNo$$ = val.consultationRoomNo;
                    val._id = _this.utilService.generateUniqueId() + "-" + index;
                });
            }
            else if (response.responseCode === 'E400') {
                _this.toaster.error('failed', 'The opertion is unsuccessful');
            }
        });
    };
    /**
     * In insert api we are replacing the null with new value
     */
    PatientsWaitingBoardComponent.prototype.insertDoctorSettings = function () {
        var _this = this;
        var payloadWithConsulationRoomId$;
        var payloadWithoutConsulationRoomId$;
        var obs$ = [];
        var payload = this.filterFunction();
        var apiMapper = function (val) {
            return val.responseCode === 'E400' ? Object(rxjs__WEBPACK_IMPORTED_MODULE_3__["throwError"])(val.responseMessage) : val;
        };
        var payloadWithConsulationRoomId = payload.filter(function (val) { return val.consultationRoomId; });
        var payloadWithoutConsulationRoomId = payload.filter(function (val) { return !val.consultationRoomId; });
        if (payloadWithoutConsulationRoomId.length) {
            payloadWithoutConsulationRoomId$ = this.opdService
                .insertDoctorSettings(payloadWithoutConsulationRoomId)
                .pipe(apiMapper);
            obs$.push(payloadWithoutConsulationRoomId$);
        }
        if (payloadWithConsulationRoomId.length) {
            payloadWithConsulationRoomId$ = this.opdService
                .updateDoctorSettings(payloadWithConsulationRoomId)
                .pipe(apiMapper);
            obs$.push(payloadWithConsulationRoomId$);
        }
        Object(rxjs__WEBPACK_IMPORTED_MODULE_3__["forkJoin"])(obs$).subscribe(function () {
            payload.forEach(function (val) {
                var foundDoctor = _this.doctors.find(function (doctor) { return val._id === doctor._id; });
                foundDoctor.consultationRoomNo$$ = val.consultationRoomNo;
            });
        }, function () {
            _this.toaster.error('failed', 'The opertion is unsuccessful');
        });
    };
    /**
     * the filter function is used to compare the room no's of a doctor, defaultly we are giving 0 as doctor room no
     * if no is not equal to 0 it will update that room no and save it to the database
     * @returns {Array< DoctorSettings>}
     */
    PatientsWaitingBoardComponent.prototype.filterFunction = function () {
        return this.doctors.filter(function (doctor) { return doctor.consultationRoomNo$$ !== doctor.consultationRoomNo; });
    };
    PatientsWaitingBoardComponent.prototype.clearFunction = function () {
        var _this = this;
        this.filterFunction().forEach(function (data) {
            var foundDoctor = _this.doctors.find(function (doctor) { return data._id === doctor._id; });
            foundDoctor.consultationRoomNo = data.consultationRoomNo$$;
        });
    };
    PatientsWaitingBoardComponent.prototype.selectFilter = function () {
        this.showFilters = !this.showFilters;
    };
    /**
     * for dropdown.
     */
    PatientsWaitingBoardComponent.prototype.getEmpListBasedOnDesignation = function () {
        var _this = this;
        this.opdService
            .getEmpListBasedOnDesignation(this.getCommonPayload2())
            .subscribe(function (Response) {
            if (Response.responseCode === 'E200') {
                _this.doctorsList = Response.data;
            }
            else if (Response.responseCode === 'E400') {
                _this.toaster.error('failed', 'this operation is unsuccessful ');
            }
        });
    };
    PatientsWaitingBoardComponent.prototype.fetchListOfSpecialities = function () {
        var _this = this;
        this.loginApiService
            .fetchListOfSpecialities(this.getCommonPayload2())
            .subscribe(function (Response) {
            if (Response.responseCode === 'E200') {
                _this.doctorsSpecialityList = Response.data;
            }
            else if (Response.responseCode === 'E400') {
                _this.toaster.error('failed', 'this operation is unsuccessful ');
            }
        });
    };
    Object.defineProperty(PatientsWaitingBoardComponent.prototype, "fallbackProfileImage", {
        get: function () {
            return 'https://s3.ap-south-1.amazonaws.com/dru.assets/images/app/icons/user-male.png';
        },
        enumerable: true,
        configurable: true
    });
    return PatientsWaitingBoardComponent;
}());



/***/ }),

/***/ "./src/app/modules/digital-board/digitalBoard-routing.module.ts":
/*!**********************************************************************!*\
  !*** ./src/app/modules/digital-board/digitalBoard-routing.module.ts ***!
  \**********************************************************************/
/*! exports provided: DigitalBoardRouterModule, ɵ0, ɵ1 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DigitalBoardRouterModule", function() { return DigitalBoardRouterModule; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ɵ0", function() { return ɵ0; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ɵ1", function() { return ɵ1; });
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _app_modules_digital_board_containers_patients_waiting_board_patients_waiting_board_component__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @app/modules/digital-board/containers/patients-waiting-board/patients-waiting-board.component */ "./src/app/modules/digital-board/containers/patients-waiting-board/patients-waiting-board.component.ts");
/* harmony import */ var _containers_display_board_display_board_component__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./containers/display-board/display-board.component */ "./src/app/modules/digital-board/containers/display-board/display-board.component.ts");



var ɵ0 = {
    title: 'Doctor Settings Screen',
}, ɵ1 = {
    title: 'Display Board'
};
var routes = [
    {
        path: 'patientsWaitingList',
        data: ɵ0,
        component: _app_modules_digital_board_containers_patients_waiting_board_patients_waiting_board_component__WEBPACK_IMPORTED_MODULE_1__["PatientsWaitingBoardComponent"]
    },
    { path: '', redirectTo: 'patientsWaitingList', pathMatch: 'prefix' },
    {
        path: 'display-board',
        data: ɵ1,
        component: _containers_display_board_display_board_component__WEBPACK_IMPORTED_MODULE_2__["DoctorsDisplayBoardComponent"]
    }
];
var DigitalBoardRouterModule = /** @class */ (function () {
    function DigitalBoardRouterModule() {
    }
    return DigitalBoardRouterModule;
}());




/***/ }),

/***/ "./src/app/modules/digital-board/digitalBoard.module.ngfactory.js":
/*!************************************************************************!*\
  !*** ./src/app/modules/digital-board/digitalBoard.module.ngfactory.js ***!
  \************************************************************************/
/*! exports provided: DigitalBoardModuleNgFactory */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DigitalBoardModuleNgFactory", function() { return DigitalBoardModuleNgFactory; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _digitalBoard_module__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./digitalBoard.module */ "./src/app/modules/digital-board/digitalBoard.module.ts");
/* harmony import */ var _node_modules_angular_router_router_ngfactory__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../node_modules/@angular/router/router.ngfactory */ "./node_modules/@angular/router/router.ngfactory.js");
/* harmony import */ var _containers_patients_waiting_board_patients_waiting_board_component_ngfactory__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./containers/patients-waiting-board/patients-waiting-board.component.ngfactory */ "./src/app/modules/digital-board/containers/patients-waiting-board/patients-waiting-board.component.ngfactory.js");
/* harmony import */ var _containers_display_board_display_board_component_ngfactory__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./containers/display-board/display-board.component.ngfactory */ "./src/app/modules/digital-board/containers/display-board/display-board.component.ngfactory.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var ngx_filter_pipe__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ngx-filter-pipe */ "./node_modules/ngx-filter-pipe/esm5/ngx-filter-pipe.js");
/* harmony import */ var _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/flex-layout/core */ "./node_modules/@angular/flex-layout/esm5/core.es5.js");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var ngx_virtual_scroller_dist_virtual_scroller__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ngx-virtual-scroller/dist/virtual-scroller */ "./node_modules/ngx-virtual-scroller/dist/virtual-scroller.js");
/* harmony import */ var ngx_virtual_scroller_dist_virtual_scroller__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(ngx_virtual_scroller_dist_virtual_scroller__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @ng-select/ng-select */ "./node_modules/@ng-select/ng-select/fesm5/ng-select.js");
/* harmony import */ var _angular_cdk_bidi__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @angular/cdk/bidi */ "./node_modules/@angular/cdk/esm5/bidi.es5.js");
/* harmony import */ var _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/flex-layout/flex */ "./node_modules/@angular/flex-layout/esm5/flex.es5.js");
/* harmony import */ var _angular_flex_layout_extended__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/flex-layout/extended */ "./node_modules/@angular/flex-layout/esm5/extended.es5.js");
/* harmony import */ var _angular_flex_layout_grid__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @angular/flex-layout/grid */ "./node_modules/@angular/flex-layout/esm5/grid.es5.js");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @angular/flex-layout */ "./node_modules/@angular/flex-layout/esm5/flex-layout.es5.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _digitalBoard_routing_module__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! ./digitalBoard-routing.module */ "./src/app/modules/digital-board/digitalBoard-routing.module.ts");
/* harmony import */ var _ngx_translate_core__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! @ngx-translate/core */ "./node_modules/@ngx-translate/core/fesm5/ngx-translate-core.js");
/* harmony import */ var _containers_patients_waiting_board_patients_waiting_board_component__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! ./containers/patients-waiting-board/patients-waiting-board.component */ "./src/app/modules/digital-board/containers/patients-waiting-board/patients-waiting-board.component.ts");
/* harmony import */ var _containers_display_board_display_board_component__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! ./containers/display-board/display-board.component */ "./src/app/modules/digital-board/containers/display-board/display-board.component.ts");
/**
 * @fileoverview This file was generated by the Angular template compiler. Do not edit.
 *
 * @suppress {suspiciousCode,uselessCode,missingProperties,missingOverride,checkTypes}
 * tslint:disable
 */ 






















var DigitalBoardModuleNgFactory = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵcmf"](_digitalBoard_module__WEBPACK_IMPORTED_MODULE_1__["DigitalBoardModule"], [], function (_l) { return _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmod"]([_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](512, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ComponentFactoryResolver"], _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵCodegenComponentFactoryResolver"], [[8, [_node_modules_angular_router_router_ngfactory__WEBPACK_IMPORTED_MODULE_2__["ɵEmptyOutletComponentNgFactory"], _containers_patients_waiting_board_patients_waiting_board_component_ngfactory__WEBPACK_IMPORTED_MODULE_3__["PatientsWaitingBoardComponentNgFactory"], _containers_display_board_display_board_component_ngfactory__WEBPACK_IMPORTED_MODULE_4__["DoctorsDisplayBoardComponentNgFactory"]]], [3, _angular_core__WEBPACK_IMPORTED_MODULE_0__["ComponentFactoryResolver"]], _angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModuleRef"]]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](4608, _angular_common__WEBPACK_IMPORTED_MODULE_5__["NgLocalization"], _angular_common__WEBPACK_IMPORTED_MODULE_5__["NgLocaleLocalization"], [_angular_core__WEBPACK_IMPORTED_MODULE_0__["LOCALE_ID"], [2, _angular_common__WEBPACK_IMPORTED_MODULE_5__["ɵangular_packages_common_common_a"]]]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](4608, ngx_filter_pipe__WEBPACK_IMPORTED_MODULE_6__["FilterPipe"], ngx_filter_pipe__WEBPACK_IMPORTED_MODULE_6__["FilterPipe"], []), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](5120, _angular_core__WEBPACK_IMPORTED_MODULE_0__["APP_BOOTSTRAP_LISTENER"], function (p0_0, p0_1) { return [_angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_7__["removeStyles"](p0_0, p0_1)]; }, [_angular_common__WEBPACK_IMPORTED_MODULE_5__["DOCUMENT"], _angular_core__WEBPACK_IMPORTED_MODULE_0__["PLATFORM_ID"]]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](4608, _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HttpXsrfTokenExtractor"], _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["ɵangular_packages_common_http_http_g"], [_angular_common__WEBPACK_IMPORTED_MODULE_5__["DOCUMENT"], _angular_core__WEBPACK_IMPORTED_MODULE_0__["PLATFORM_ID"], _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["ɵangular_packages_common_http_http_e"]]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](4608, _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["ɵangular_packages_common_http_http_h"], _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["ɵangular_packages_common_http_http_h"], [_angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HttpXsrfTokenExtractor"], _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["ɵangular_packages_common_http_http_f"]]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](5120, _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HTTP_INTERCEPTORS"], function (p0_0) { return [p0_0]; }, [_angular_common_http__WEBPACK_IMPORTED_MODULE_8__["ɵangular_packages_common_http_http_h"]]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](4608, _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["ɵangular_packages_common_http_http_d"], _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["ɵangular_packages_common_http_http_d"], []), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](6144, _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["XhrFactory"], null, [_angular_common_http__WEBPACK_IMPORTED_MODULE_8__["ɵangular_packages_common_http_http_d"]]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](4608, _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HttpXhrBackend"], _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HttpXhrBackend"], [_angular_common_http__WEBPACK_IMPORTED_MODULE_8__["XhrFactory"]]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](6144, _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HttpBackend"], null, [_angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HttpXhrBackend"]]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](4608, _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HttpHandler"], _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["ɵHttpInterceptingHandler"], [_angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HttpBackend"], _angular_core__WEBPACK_IMPORTED_MODULE_0__["Injector"]]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](4608, _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HttpClient"], _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HttpClient"], [_angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HttpHandler"]]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](4608, _angular_forms__WEBPACK_IMPORTED_MODULE_9__["ɵangular_packages_forms_forms_j"], _angular_forms__WEBPACK_IMPORTED_MODULE_9__["ɵangular_packages_forms_forms_j"], []), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](1073742336, _angular_common__WEBPACK_IMPORTED_MODULE_5__["CommonModule"], _angular_common__WEBPACK_IMPORTED_MODULE_5__["CommonModule"], []), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](1073742336, ngx_virtual_scroller_dist_virtual_scroller__WEBPACK_IMPORTED_MODULE_10__["VirtualScrollerModule"], ngx_virtual_scroller_dist_virtual_scroller__WEBPACK_IMPORTED_MODULE_10__["VirtualScrollerModule"], []), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](1073742336, _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_11__["NgSelectModule"], _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_11__["NgSelectModule"], []), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](1073742336, ngx_filter_pipe__WEBPACK_IMPORTED_MODULE_6__["FilterPipeModule"], ngx_filter_pipe__WEBPACK_IMPORTED_MODULE_6__["FilterPipeModule"], []), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](1073742336, _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_7__["CoreModule"], _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_7__["CoreModule"], []), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](1073742336, _angular_cdk_bidi__WEBPACK_IMPORTED_MODULE_12__["BidiModule"], _angular_cdk_bidi__WEBPACK_IMPORTED_MODULE_12__["BidiModule"], []), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](1073742336, _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_13__["FlexModule"], _angular_flex_layout_flex__WEBPACK_IMPORTED_MODULE_13__["FlexModule"], []), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](1073742336, _angular_flex_layout_extended__WEBPACK_IMPORTED_MODULE_14__["ExtendedModule"], _angular_flex_layout_extended__WEBPACK_IMPORTED_MODULE_14__["ExtendedModule"], []), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](1073742336, _angular_flex_layout_grid__WEBPACK_IMPORTED_MODULE_15__["GridModule"], _angular_flex_layout_grid__WEBPACK_IMPORTED_MODULE_15__["GridModule"], []), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](1073742336, _angular_flex_layout__WEBPACK_IMPORTED_MODULE_16__["FlexLayoutModule"], _angular_flex_layout__WEBPACK_IMPORTED_MODULE_16__["FlexLayoutModule"], [[2, _angular_flex_layout_core__WEBPACK_IMPORTED_MODULE_7__["SERVER_TOKEN"]], _angular_core__WEBPACK_IMPORTED_MODULE_0__["PLATFORM_ID"]]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](1073742336, _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HttpClientXsrfModule"], _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HttpClientXsrfModule"], []), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](1073742336, _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HttpClientModule"], _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HttpClientModule"], []), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](1073742336, _angular_forms__WEBPACK_IMPORTED_MODULE_9__["ɵangular_packages_forms_forms_bc"], _angular_forms__WEBPACK_IMPORTED_MODULE_9__["ɵangular_packages_forms_forms_bc"], []), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](1073742336, _angular_forms__WEBPACK_IMPORTED_MODULE_9__["FormsModule"], _angular_forms__WEBPACK_IMPORTED_MODULE_9__["FormsModule"], []), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](1073742336, _angular_router__WEBPACK_IMPORTED_MODULE_17__["RouterModule"], _angular_router__WEBPACK_IMPORTED_MODULE_17__["RouterModule"], [[2, _angular_router__WEBPACK_IMPORTED_MODULE_17__["ɵangular_packages_router_router_a"]], [2, _angular_router__WEBPACK_IMPORTED_MODULE_17__["Router"]]]), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](1073742336, _digitalBoard_routing_module__WEBPACK_IMPORTED_MODULE_18__["DigitalBoardRouterModule"], _digitalBoard_routing_module__WEBPACK_IMPORTED_MODULE_18__["DigitalBoardRouterModule"], []), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](1073742336, _ngx_translate_core__WEBPACK_IMPORTED_MODULE_19__["TranslateModule"], _ngx_translate_core__WEBPACK_IMPORTED_MODULE_19__["TranslateModule"], []), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](1073742336, _digitalBoard_module__WEBPACK_IMPORTED_MODULE_1__["DigitalBoardModule"], _digitalBoard_module__WEBPACK_IMPORTED_MODULE_1__["DigitalBoardModule"], []), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](256, _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_11__["SELECTION_MODEL_FACTORY"], _ng_select_ng_select__WEBPACK_IMPORTED_MODULE_11__["ɵb"], []), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](256, _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["ɵangular_packages_common_http_http_e"], "XSRF-TOKEN", []), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](256, _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["ɵangular_packages_common_http_http_f"], "X-XSRF-TOKEN", []), _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵmpd"](1024, _angular_router__WEBPACK_IMPORTED_MODULE_17__["ROUTES"], function () { return [[{ path: "patientsWaitingList", data: _digitalBoard_routing_module__WEBPACK_IMPORTED_MODULE_18__["ɵ0"], component: _containers_patients_waiting_board_patients_waiting_board_component__WEBPACK_IMPORTED_MODULE_20__["PatientsWaitingBoardComponent"] }, { path: "", redirectTo: "patientsWaitingList", pathMatch: "prefix" }, { path: "display-board", data: _digitalBoard_routing_module__WEBPACK_IMPORTED_MODULE_18__["ɵ1"], component: _containers_display_board_display_board_component__WEBPACK_IMPORTED_MODULE_21__["DoctorsDisplayBoardComponent"] }]]; }, [])]); });



/***/ }),

/***/ "./src/app/modules/digital-board/digitalBoard.module.ts":
/*!**************************************************************!*\
  !*** ./src/app/modules/digital-board/digitalBoard.module.ts ***!
  \**************************************************************/
/*! exports provided: DigitalBoardModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DigitalBoardModule", function() { return DigitalBoardModule; });
var DigitalBoardModule = /** @class */ (function () {
    function DigitalBoardModule() {
    }
    return DigitalBoardModule;
}());



/***/ }),

/***/ "./src/app/modules/digital-board/pipes/doctor-filter.pipe.ts":
/*!*******************************************************************!*\
  !*** ./src/app/modules/digital-board/pipes/doctor-filter.pipe.ts ***!
  \*******************************************************************/
/*! exports provided: DoctorFilterPipe */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DoctorFilterPipe", function() { return DoctorFilterPipe; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");

var DoctorFilterPipe = /** @class */ (function () {
    function DoctorFilterPipe(arrayIntersector) {
        this.arrayIntersector = arrayIntersector;
    }
    DoctorFilterPipe.prototype.transform = function (doctors, searchItem) {
        var _this = this;
        return doctors.filter(function (doctor) {
            var passed = true;
            if (searchItem.specialityId.$or && doctor.specialityId) {
                var doctorSpecialties = doctor.speciality.split(",");
                var intersection = _this.arrayIntersector(searchItem.specialityId.$or, doctorSpecialties);
                passed = !!intersection.length;
            }
            if (searchItem.doctorId.$or && doctor.doctorId) {
                passed = searchItem.doctorId.$or.includes(doctor.doctorId);
            }
            return passed;
        });
    };
    return DoctorFilterPipe;
}());



/***/ })

}]);
//# sourceMappingURL=modules-digital-board-digitalBoard-module-ngfactory.js.map