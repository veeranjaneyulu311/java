/******/ (function(modules) { // webpackBootstrap
/******/ 	// install a JSONP callback for chunk loading
/******/ 	function webpackJsonpCallback(data) {
/******/ 		var chunkIds = data[0];
/******/ 		var moreModules = data[1];
/******/ 		var executeModules = data[2];
/******/
/******/ 		// add "moreModules" to the modules object,
/******/ 		// then flag all "chunkIds" as loaded and fire callback
/******/ 		var moduleId, chunkId, i = 0, resolves = [];
/******/ 		for(;i < chunkIds.length; i++) {
/******/ 			chunkId = chunkIds[i];
/******/ 			if(installedChunks[chunkId]) {
/******/ 				resolves.push(installedChunks[chunkId][0]);
/******/ 			}
/******/ 			installedChunks[chunkId] = 0;
/******/ 		}
/******/ 		for(moduleId in moreModules) {
/******/ 			if(Object.prototype.hasOwnProperty.call(moreModules, moduleId)) {
/******/ 				modules[moduleId] = moreModules[moduleId];
/******/ 			}
/******/ 		}
/******/ 		if(parentJsonpFunction) parentJsonpFunction(data);
/******/
/******/ 		while(resolves.length) {
/******/ 			resolves.shift()();
/******/ 		}
/******/
/******/ 		// add entry modules from loaded chunk to deferred list
/******/ 		deferredModules.push.apply(deferredModules, executeModules || []);
/******/
/******/ 		// run deferred modules when all chunks ready
/******/ 		return checkDeferredModules();
/******/ 	};
/******/ 	function checkDeferredModules() {
/******/ 		var result;
/******/ 		for(var i = 0; i < deferredModules.length; i++) {
/******/ 			var deferredModule = deferredModules[i];
/******/ 			var fulfilled = true;
/******/ 			for(var j = 1; j < deferredModule.length; j++) {
/******/ 				var depId = deferredModule[j];
/******/ 				if(installedChunks[depId] !== 0) fulfilled = false;
/******/ 			}
/******/ 			if(fulfilled) {
/******/ 				deferredModules.splice(i--, 1);
/******/ 				result = __webpack_require__(__webpack_require__.s = deferredModule[0]);
/******/ 			}
/******/ 		}
/******/ 		return result;
/******/ 	}
/******/
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// object to store loaded and loading chunks
/******/ 	// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 	// Promise = chunk loading, 0 = chunk loaded
/******/ 	var installedChunks = {
/******/ 		"runtime": 0
/******/ 	};
/******/
/******/ 	var deferredModules = [];
/******/
/******/ 	// script path function
/******/ 	function jsonpScriptSrc(chunkId) {
/******/ 		return __webpack_require__.p + "" + ({"default~modules-Inventory-inventory-module-ngfactory~modules-appointment-appointment-module-ngfactor~62e1467c":"default~modules-Inventory-inventory-module-ngfactory~modules-appointment-appointment-module-ngfactor~62e1467c","default~modules-Inventory-inventory-module-ngfactory~modules-appointment-appointment-module-ngfactor~c764971b":"default~modules-Inventory-inventory-module-ngfactory~modules-appointment-appointment-module-ngfactor~c764971b","default~modules-Inventory-inventory-module-ngfactory~modules-appointment-appointment-module-ngfactor~541f3444":"default~modules-Inventory-inventory-module-ngfactory~modules-appointment-appointment-module-ngfactor~541f3444","default~modules-Inventory-inventory-module-ngfactory~modules-appointment-appointment-module-ngfactor~419f9d80":"default~modules-Inventory-inventory-module-ngfactory~modules-appointment-appointment-module-ngfactor~419f9d80","default~modules-Inventory-inventory-module-ngfactory~modules-mis-mis-module-ngfactory~modules-optica~eee758db":"default~modules-Inventory-inventory-module-ngfactory~modules-mis-mis-module-ngfactory~modules-optica~eee758db","common":"common","modules-Inventory-inventory-module-ngfactory":"modules-Inventory-inventory-module-ngfactory","default~modules-appointment-appointment-module-ngfactory~modules-counselling-counselling-module-ngfa~2e4863b2":"default~modules-appointment-appointment-module-ngfactory~modules-counselling-counselling-module-ngfa~2e4863b2","default~modules-appointment-appointment-module-ngfactory~modules-counselling-counselling-module-ngfa~9fc51d31":"default~modules-appointment-appointment-module-ngfactory~modules-counselling-counselling-module-ngfa~9fc51d31","modules-counselling-counselling-module-ngfactory":"modules-counselling-counselling-module-ngfactory","modules-discharge-summary-discharge-summary-module-ngfactory":"modules-discharge-summary-discharge-summary-module-ngfactory","default~modules-emr-ophthalmology-emr-ophthalmology-module-ngfactory~modules-imaging-imaging-module-~0ba9de66":"default~modules-emr-ophthalmology-emr-ophthalmology-module-ngfactory~modules-imaging-imaging-module-~0ba9de66","default~modules-appointment-appointment-module-ngfactory~modules-digital-board-digitalBoard-module-n~1f7e2e24":"default~modules-appointment-appointment-module-ngfactory~modules-digital-board-digitalBoard-module-n~1f7e2e24","default~modules-imaging-imaging-module-ngfactory~modules-optical-store-opticalStore-module-ngfactory":"default~modules-imaging-imaging-module-ngfactory~modules-optical-store-opticalStore-module-ngfactory","modules-imaging-imaging-module-ngfactory":"modules-imaging-imaging-module-ngfactory","default~modules-appointment-appointment-module-ngfactory~modules-digital-board-digitalBoard-module-n~4d269708":"default~modules-appointment-appointment-module-ngfactory~modules-digital-board-digitalBoard-module-n~4d269708","default~modules-appointment-appointment-module-ngfactory~modules-emr-ophthalmology-emr-ophthalmology~fde66369":"default~modules-appointment-appointment-module-ngfactory~modules-emr-ophthalmology-emr-ophthalmology~fde66369","default~modules-appointment-appointment-module-ngfactory~modules-emr-ophthalmology-emr-ophthalmology~b61fee0a":"default~modules-appointment-appointment-module-ngfactory~modules-emr-ophthalmology-emr-ophthalmology~b61fee0a","default~modules-appointment-appointment-module-ngfactory~modules-optical-store-opticalStore-module-n~a7d660d3":"default~modules-appointment-appointment-module-ngfactory~modules-optical-store-opticalStore-module-n~a7d660d3","modules-appointment-appointment-module-ngfactory":"modules-appointment-appointment-module-ngfactory","modules-opd-opd-module-ngfactory":"modules-opd-opd-module-ngfactory","modules-emr-ophthalmology-emr-ophthalmology-module-ngfactory":"modules-emr-ophthalmology-emr-ophthalmology-module-ngfactory","default~modules-optical-store-opticalStore-module-ngfactory~modules-warehouse-warehouse-module-ngfac~a483f32c":"default~modules-optical-store-opticalStore-module-ngfactory~modules-warehouse-warehouse-module-ngfac~a483f32c","modules-optical-store-opticalStore-module-ngfactory":"modules-optical-store-opticalStore-module-ngfactory","modules-warehouse-warehouse-module-ngfactory":"modules-warehouse-warehouse-module-ngfactory","modules-statutory-statutory-module-ngfactory":"modules-statutory-statutory-module-ngfactory","default~modules-digital-board-digitalBoard-module-ngfactory~modules-mis-mis-module-ngfactory":"default~modules-digital-board-digitalBoard-module-ngfactory~modules-mis-mis-module-ngfactory","modules-mis-mis-module-ngfactory":"modules-mis-mis-module-ngfactory","modules-opd-status-opd-status-module-ngfactory":"modules-opd-status-opd-status-module-ngfactory","modules-digital-board-digitalBoard-module-ngfactory":"modules-digital-board-digitalBoard-module-ngfactory"}[chunkId]||chunkId) + ".js"
/******/ 	}
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/ 	// This file contains only the entry chunk.
/******/ 	// The chunk loading function for additional chunks
/******/ 	__webpack_require__.e = function requireEnsure(chunkId) {
/******/ 		var promises = [];
/******/
/******/
/******/ 		// JSONP chunk loading for javascript
/******/
/******/ 		var installedChunkData = installedChunks[chunkId];
/******/ 		if(installedChunkData !== 0) { // 0 means "already installed".
/******/
/******/ 			// a Promise means "currently loading".
/******/ 			if(installedChunkData) {
/******/ 				promises.push(installedChunkData[2]);
/******/ 			} else {
/******/ 				// setup Promise in chunk cache
/******/ 				var promise = new Promise(function(resolve, reject) {
/******/ 					installedChunkData = installedChunks[chunkId] = [resolve, reject];
/******/ 				});
/******/ 				promises.push(installedChunkData[2] = promise);
/******/
/******/ 				// start chunk loading
/******/ 				var script = document.createElement('script');
/******/ 				var onScriptComplete;
/******/
/******/ 				script.charset = 'utf-8';
/******/ 				script.timeout = 120;
/******/ 				if (__webpack_require__.nc) {
/******/ 					script.setAttribute("nonce", __webpack_require__.nc);
/******/ 				}
/******/ 				script.src = jsonpScriptSrc(chunkId);
/******/
/******/ 				onScriptComplete = function (event) {
/******/ 					// avoid mem leaks in IE.
/******/ 					script.onerror = script.onload = null;
/******/ 					clearTimeout(timeout);
/******/ 					var chunk = installedChunks[chunkId];
/******/ 					if(chunk !== 0) {
/******/ 						if(chunk) {
/******/ 							var errorType = event && (event.type === 'load' ? 'missing' : event.type);
/******/ 							var realSrc = event && event.target && event.target.src;
/******/ 							var error = new Error('Loading chunk ' + chunkId + ' failed.\n(' + errorType + ': ' + realSrc + ')');
/******/ 							error.type = errorType;
/******/ 							error.request = realSrc;
/******/ 							chunk[1](error);
/******/ 						}
/******/ 						installedChunks[chunkId] = undefined;
/******/ 					}
/******/ 				};
/******/ 				var timeout = setTimeout(function(){
/******/ 					onScriptComplete({ type: 'timeout', target: script });
/******/ 				}, 120000);
/******/ 				script.onerror = script.onload = onScriptComplete;
/******/ 				document.head.appendChild(script);
/******/ 			}
/******/ 		}
/******/ 		return Promise.all(promises);
/******/ 	};
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// on error function for async loading
/******/ 	__webpack_require__.oe = function(err) { console.error(err); throw err; };
/******/
/******/ 	var jsonpArray = window["webpackJsonp"] = window["webpackJsonp"] || [];
/******/ 	var oldJsonpFunction = jsonpArray.push.bind(jsonpArray);
/******/ 	jsonpArray.push = webpackJsonpCallback;
/******/ 	jsonpArray = jsonpArray.slice();
/******/ 	for(var i = 0; i < jsonpArray.length; i++) webpackJsonpCallback(jsonpArray[i]);
/******/ 	var parentJsonpFunction = oldJsonpFunction;
/******/
/******/
/******/ 	// run deferred modules from other chunks
/******/ 	checkDeferredModules();
/******/ })
/************************************************************************/
/******/ ([]);
//# sourceMappingURL=runtime.js.map