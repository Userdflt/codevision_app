/*
 * ATTENTION: An "eval-source-map" devtool has been used.
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file with attached SourceMaps in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
(() => {
var exports = {};
exports.id = "pages/_app";
exports.ids = ["pages/_app"];
exports.modules = {

/***/ "(pages-dir-node)/./pages/_app.tsx":
/*!************************!*\
  !*** ./pages/_app.tsx ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (/* binding */ App),\n/* harmony export */   useSupabase: () => (/* binding */ useSupabase)\n/* harmony export */ });\n/* harmony import */ var react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-dev-runtime */ \"react/jsx-dev-runtime\");\n/* harmony import */ var react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _supabase_ssr__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @supabase/ssr */ \"@supabase/ssr\");\n/* harmony import */ var _supabase_ssr__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_supabase_ssr__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ \"react\");\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);\n/* harmony import */ var next_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! next/router */ \"(pages-dir-node)/./node_modules/next/router.js\");\n/* harmony import */ var next_router__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(next_router__WEBPACK_IMPORTED_MODULE_3__);\n/* harmony import */ var _styles_globals_css__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../styles/globals.css */ \"(pages-dir-node)/./styles/globals.css\");\n/* harmony import */ var _styles_globals_css__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_styles_globals_css__WEBPACK_IMPORTED_MODULE_4__);\n// frontend/pages/_app.tsx\n\n\n\n\n\nconst SupabaseContext = /*#__PURE__*/ (0,react__WEBPACK_IMPORTED_MODULE_2__.createContext)(undefined);\nfunction useSupabase() {\n    const context = (0,react__WEBPACK_IMPORTED_MODULE_2__.useContext)(SupabaseContext);\n    if (!context) {\n        throw new Error('useSupabase must be used within a SupabaseProvider');\n    }\n    return context;\n}\nfunction App({ Component, pageProps }) {\n    const router = (0,next_router__WEBPACK_IMPORTED_MODULE_3__.useRouter)();\n    const [supabase] = (0,react__WEBPACK_IMPORTED_MODULE_2__.useState)({\n        \"App.useState\": ()=>(0,_supabase_ssr__WEBPACK_IMPORTED_MODULE_1__.createBrowserClient)(\"https://evxduxdszbxukcjocizl.supabase.co\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV2eGR1eGRzemJ4dWtjam9jaXpsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEwNzA2OTAsImV4cCI6MjA2NjY0NjY5MH0.zo_0ObG0aNxCdh6QU5WxmBNU3sPf0eyBEIsnq0LhxWE\")\n    }[\"App.useState\"]);\n    // Prevent automatic session checking on reset-password page\n    (0,react__WEBPACK_IMPORTED_MODULE_2__.useEffect)({\n        \"App.useEffect\": ()=>{\n            if (router.pathname === '/reset-password') {\n                console.log('Skipping auto session check on reset-password page');\n                return; // Don't auto-check session on reset page\n            }\n            // Auto-check session for other pages\n            const checkSession = {\n                \"App.useEffect.checkSession\": async ()=>{\n                    try {\n                        console.log('Auto-checking session for page:', router.pathname);\n                        await supabase.auth.getSession();\n                    } catch (error) {\n                        console.warn('Session check failed:', error);\n                    }\n                }\n            }[\"App.useEffect.checkSession\"];\n            checkSession();\n        }\n    }[\"App.useEffect\"], [\n        router.pathname,\n        supabase\n    ]);\n    return /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(SupabaseContext.Provider, {\n        value: {\n            supabase,\n            session: null,\n            user: null\n        },\n        children: /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(Component, {\n            ...pageProps\n        }, void 0, false, {\n            fileName: \"/Volumes/Work(SSD)/Personal Projects/codevision_app/codevision_app/frontend/pages/_app.tsx\",\n            lineNumber: 51,\n            columnNumber: 7\n        }, this)\n    }, void 0, false, {\n        fileName: \"/Volumes/Work(SSD)/Personal Projects/codevision_app/codevision_app/frontend/pages/_app.tsx\",\n        lineNumber: 50,\n        columnNumber: 5\n    }, this);\n}\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKHBhZ2VzLWRpci1ub2RlKS8uL3BhZ2VzL19hcHAudHN4IiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBCQUEwQjs7QUFDeUI7QUFFbUI7QUFFL0I7QUFDVDtBQUc5QixNQUFNTSxnQ0FBa0JMLG9EQUFhQSxDQUFrQ007QUFFaEUsU0FBU0M7SUFDZCxNQUFNQyxVQUFVUCxpREFBVUEsQ0FBQ0k7SUFDM0IsSUFBSSxDQUFDRyxTQUFTO1FBQ1osTUFBTSxJQUFJQyxNQUFNO0lBQ2xCO0lBQ0EsT0FBT0Q7QUFDVDtBQUVlLFNBQVNFLElBQUksRUFBRUMsU0FBUyxFQUFFQyxTQUFTLEVBQVk7SUFDNUQsTUFBTUMsU0FBU1Qsc0RBQVNBO0lBQ3hCLE1BQU0sQ0FBQ1UsU0FBUyxHQUFHWCwrQ0FBUUE7d0JBQWlCLElBQzFDSixrRUFBbUJBLENBQ2pCZ0IsMENBQW9DLEVBQ3BDQSxrTkFBeUM7O0lBSTdDLDREQUE0RDtJQUM1RGIsZ0RBQVNBO3lCQUFDO1lBQ1IsSUFBSVcsT0FBT00sUUFBUSxLQUFLLG1CQUFtQjtnQkFDekNDLFFBQVFDLEdBQUcsQ0FBQztnQkFDWixRQUFPLHlDQUF5QztZQUNsRDtZQUVBLHFDQUFxQztZQUNyQyxNQUFNQzs4Q0FBZTtvQkFDbkIsSUFBSTt3QkFDRkYsUUFBUUMsR0FBRyxDQUFDLG1DQUFtQ1IsT0FBT00sUUFBUTt3QkFDOUQsTUFBTUwsU0FBU1MsSUFBSSxDQUFDQyxVQUFVO29CQUNoQyxFQUFFLE9BQU9DLE9BQU87d0JBQ2RMLFFBQVFNLElBQUksQ0FBQyx5QkFBeUJEO29CQUN4QztnQkFDRjs7WUFFQUg7UUFDRjt3QkFBRztRQUFDVCxPQUFPTSxRQUFRO1FBQUVMO0tBQVM7SUFFOUIscUJBQ0UsOERBQUNULGdCQUFnQnNCLFFBQVE7UUFBQ0MsT0FBTztZQUFFZDtZQUFVZSxTQUFTO1lBQU1DLE1BQU07UUFBSztrQkFDckUsNEVBQUNuQjtZQUFXLEdBQUdDLFNBQVM7Ozs7Ozs7Ozs7O0FBRzlCIiwic291cmNlcyI6WyIvVm9sdW1lcy9Xb3JrKFNTRCkvUGVyc29uYWwgUHJvamVjdHMvY29kZXZpc2lvbl9hcHAvY29kZXZpc2lvbl9hcHAvZnJvbnRlbmQvcGFnZXMvX2FwcC50c3giXSwic291cmNlc0NvbnRlbnQiOlsiLy8gZnJvbnRlbmQvcGFnZXMvX2FwcC50c3hcbmltcG9ydCB7IGNyZWF0ZUJyb3dzZXJDbGllbnQgfSBmcm9tICdAc3VwYWJhc2Uvc3NyJ1xuaW1wb3J0IHR5cGUgeyBTdXBhYmFzZUNsaWVudCB9IGZyb20gJ0BzdXBhYmFzZS9zdXBhYmFzZS1qcydcbmltcG9ydCB7IGNyZWF0ZUNvbnRleHQsIHVzZUNvbnRleHQsIHVzZUVmZmVjdCwgdXNlU3RhdGUgfSBmcm9tICdyZWFjdCdcbmltcG9ydCB0eXBlIHsgQXBwUHJvcHMgfSBmcm9tICduZXh0L2FwcCdcbmltcG9ydCB7IHVzZVJvdXRlciB9IGZyb20gJ25leHQvcm91dGVyJ1xuaW1wb3J0ICcuLi9zdHlsZXMvZ2xvYmFscy5jc3MnXG5pbXBvcnQgeyBTdXBhYmFzZUNvbnRleHRUeXBlIH0gZnJvbSAnLi4vbGliL3R5cGVzJ1xuXG5jb25zdCBTdXBhYmFzZUNvbnRleHQgPSBjcmVhdGVDb250ZXh0PFN1cGFiYXNlQ29udGV4dFR5cGUgfCB1bmRlZmluZWQ+KHVuZGVmaW5lZClcblxuZXhwb3J0IGZ1bmN0aW9uIHVzZVN1cGFiYXNlKCk6IFN1cGFiYXNlQ29udGV4dFR5cGUge1xuICBjb25zdCBjb250ZXh0ID0gdXNlQ29udGV4dChTdXBhYmFzZUNvbnRleHQpXG4gIGlmICghY29udGV4dCkge1xuICAgIHRocm93IG5ldyBFcnJvcigndXNlU3VwYWJhc2UgbXVzdCBiZSB1c2VkIHdpdGhpbiBhIFN1cGFiYXNlUHJvdmlkZXInKVxuICB9XG4gIHJldHVybiBjb250ZXh0XG59XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIEFwcCh7IENvbXBvbmVudCwgcGFnZVByb3BzIH06IEFwcFByb3BzKSB7XG4gIGNvbnN0IHJvdXRlciA9IHVzZVJvdXRlcigpXG4gIGNvbnN0IFtzdXBhYmFzZV0gPSB1c2VTdGF0ZTxTdXBhYmFzZUNsaWVudD4oKCkgPT5cbiAgICBjcmVhdGVCcm93c2VyQ2xpZW50KFxuICAgICAgcHJvY2Vzcy5lbnYuTkVYVF9QVUJMSUNfU1VQQUJBU0VfVVJMISxcbiAgICAgIHByb2Nlc3MuZW52Lk5FWFRfUFVCTElDX1NVUEFCQVNFX0FOT05fS0VZIVxuICAgIClcbiAgKVxuXG4gIC8vIFByZXZlbnQgYXV0b21hdGljIHNlc3Npb24gY2hlY2tpbmcgb24gcmVzZXQtcGFzc3dvcmQgcGFnZVxuICB1c2VFZmZlY3QoKCkgPT4ge1xuICAgIGlmIChyb3V0ZXIucGF0aG5hbWUgPT09ICcvcmVzZXQtcGFzc3dvcmQnKSB7XG4gICAgICBjb25zb2xlLmxvZygnU2tpcHBpbmcgYXV0byBzZXNzaW9uIGNoZWNrIG9uIHJlc2V0LXBhc3N3b3JkIHBhZ2UnKVxuICAgICAgcmV0dXJuIC8vIERvbid0IGF1dG8tY2hlY2sgc2Vzc2lvbiBvbiByZXNldCBwYWdlXG4gICAgfVxuXG4gICAgLy8gQXV0by1jaGVjayBzZXNzaW9uIGZvciBvdGhlciBwYWdlc1xuICAgIGNvbnN0IGNoZWNrU2Vzc2lvbiA9IGFzeW5jICgpID0+IHtcbiAgICAgIHRyeSB7XG4gICAgICAgIGNvbnNvbGUubG9nKCdBdXRvLWNoZWNraW5nIHNlc3Npb24gZm9yIHBhZ2U6Jywgcm91dGVyLnBhdGhuYW1lKVxuICAgICAgICBhd2FpdCBzdXBhYmFzZS5hdXRoLmdldFNlc3Npb24oKVxuICAgICAgfSBjYXRjaCAoZXJyb3IpIHtcbiAgICAgICAgY29uc29sZS53YXJuKCdTZXNzaW9uIGNoZWNrIGZhaWxlZDonLCBlcnJvcilcbiAgICAgIH1cbiAgICB9XG5cbiAgICBjaGVja1Nlc3Npb24oKVxuICB9LCBbcm91dGVyLnBhdGhuYW1lLCBzdXBhYmFzZV0pXG5cbiAgcmV0dXJuIChcbiAgICA8U3VwYWJhc2VDb250ZXh0LlByb3ZpZGVyIHZhbHVlPXt7IHN1cGFiYXNlLCBzZXNzaW9uOiBudWxsLCB1c2VyOiBudWxsIH19PlxuICAgICAgPENvbXBvbmVudCB7Li4ucGFnZVByb3BzfSAvPlxuICAgIDwvU3VwYWJhc2VDb250ZXh0LlByb3ZpZGVyPlxuICApXG59Il0sIm5hbWVzIjpbImNyZWF0ZUJyb3dzZXJDbGllbnQiLCJjcmVhdGVDb250ZXh0IiwidXNlQ29udGV4dCIsInVzZUVmZmVjdCIsInVzZVN0YXRlIiwidXNlUm91dGVyIiwiU3VwYWJhc2VDb250ZXh0IiwidW5kZWZpbmVkIiwidXNlU3VwYWJhc2UiLCJjb250ZXh0IiwiRXJyb3IiLCJBcHAiLCJDb21wb25lbnQiLCJwYWdlUHJvcHMiLCJyb3V0ZXIiLCJzdXBhYmFzZSIsInByb2Nlc3MiLCJlbnYiLCJORVhUX1BVQkxJQ19TVVBBQkFTRV9VUkwiLCJORVhUX1BVQkxJQ19TVVBBQkFTRV9BTk9OX0tFWSIsInBhdGhuYW1lIiwiY29uc29sZSIsImxvZyIsImNoZWNrU2Vzc2lvbiIsImF1dGgiLCJnZXRTZXNzaW9uIiwiZXJyb3IiLCJ3YXJuIiwiUHJvdmlkZXIiLCJ2YWx1ZSIsInNlc3Npb24iLCJ1c2VyIl0sImlnbm9yZUxpc3QiOltdLCJzb3VyY2VSb290IjoiIn0=\n//# sourceURL=webpack-internal:///(pages-dir-node)/./pages/_app.tsx\n");

/***/ }),

/***/ "(pages-dir-node)/./styles/globals.css":
/*!****************************!*\
  !*** ./styles/globals.css ***!
  \****************************/
/***/ (() => {



/***/ }),

/***/ "@supabase/ssr":
/*!********************************!*\
  !*** external "@supabase/ssr" ***!
  \********************************/
/***/ ((module) => {

"use strict";
module.exports = require("@supabase/ssr");

/***/ }),

/***/ "fs":
/*!*********************!*\
  !*** external "fs" ***!
  \*********************/
/***/ ((module) => {

"use strict";
module.exports = require("fs");

/***/ }),

/***/ "next/dist/compiled/next-server/pages.runtime.dev.js":
/*!**********************************************************************!*\
  !*** external "next/dist/compiled/next-server/pages.runtime.dev.js" ***!
  \**********************************************************************/
/***/ ((module) => {

"use strict";
module.exports = require("next/dist/compiled/next-server/pages.runtime.dev.js");

/***/ }),

/***/ "react":
/*!************************!*\
  !*** external "react" ***!
  \************************/
/***/ ((module) => {

"use strict";
module.exports = require("react");

/***/ }),

/***/ "react-dom":
/*!****************************!*\
  !*** external "react-dom" ***!
  \****************************/
/***/ ((module) => {

"use strict";
module.exports = require("react-dom");

/***/ }),

/***/ "react/jsx-dev-runtime":
/*!****************************************!*\
  !*** external "react/jsx-dev-runtime" ***!
  \****************************************/
/***/ ((module) => {

"use strict";
module.exports = require("react/jsx-dev-runtime");

/***/ }),

/***/ "react/jsx-runtime":
/*!************************************!*\
  !*** external "react/jsx-runtime" ***!
  \************************************/
/***/ ((module) => {

"use strict";
module.exports = require("react/jsx-runtime");

/***/ }),

/***/ "stream":
/*!*************************!*\
  !*** external "stream" ***!
  \*************************/
/***/ ((module) => {

"use strict";
module.exports = require("stream");

/***/ }),

/***/ "zlib":
/*!***********************!*\
  !*** external "zlib" ***!
  \***********************/
/***/ ((module) => {

"use strict";
module.exports = require("zlib");

/***/ })

};
;

// load runtime
var __webpack_require__ = require("../webpack-runtime.js");
__webpack_require__.C(exports);
var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
var __webpack_exports__ = __webpack_require__.X(0, ["vendor-chunks/next"], () => (__webpack_exec__("(pages-dir-node)/./pages/_app.tsx")));
module.exports = __webpack_exports__;

})();