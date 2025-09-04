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
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (/* binding */ App),\n/* harmony export */   useSupabase: () => (/* binding */ useSupabase)\n/* harmony export */ });\n/* harmony import */ var react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-dev-runtime */ \"react/jsx-dev-runtime\");\n/* harmony import */ var react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _supabase_ssr__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @supabase/ssr */ \"@supabase/ssr\");\n/* harmony import */ var _supabase_ssr__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_supabase_ssr__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ \"react\");\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);\n/* harmony import */ var next_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! next/router */ \"(pages-dir-node)/./node_modules/next/router.js\");\n/* harmony import */ var next_router__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(next_router__WEBPACK_IMPORTED_MODULE_3__);\n/* harmony import */ var _styles_globals_css__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../styles/globals.css */ \"(pages-dir-node)/./styles/globals.css\");\n/* harmony import */ var _styles_globals_css__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_styles_globals_css__WEBPACK_IMPORTED_MODULE_4__);\n// frontend/pages/_app.tsx\n\n\n\n\n\nconst SupabaseContext = /*#__PURE__*/ (0,react__WEBPACK_IMPORTED_MODULE_2__.createContext)(undefined);\nfunction useSupabase() {\n    const context = (0,react__WEBPACK_IMPORTED_MODULE_2__.useContext)(SupabaseContext);\n    if (!context) {\n        throw new Error('useSupabase must be used within a SupabaseProvider');\n    }\n    return context;\n}\nfunction App({ Component, pageProps }) {\n    const router = (0,next_router__WEBPACK_IMPORTED_MODULE_3__.useRouter)();\n    const [supabase] = (0,react__WEBPACK_IMPORTED_MODULE_2__.useState)({\n        \"App.useState\": ()=>(0,_supabase_ssr__WEBPACK_IMPORTED_MODULE_1__.createBrowserClient)(\"https://evxduxdszbxukcjocizl.supabase.co\", \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV2eGR1eGRzemJ4dWtjam9jaXpsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEwNzA2OTAsImV4cCI6MjA2NjY0NjY5MH0.zo_0ObG0aNxCdh6QU5WxmBNU3sPf0eyBEIsnq0LhxWE\")\n    }[\"App.useState\"]);\n    // Prevent automatic session checking on reset-password page\n    (0,react__WEBPACK_IMPORTED_MODULE_2__.useEffect)({\n        \"App.useEffect\": ()=>{\n            if (router.pathname === '/reset-password' || router.pathname === '/confirm-email') {\n                console.log('Skipping auto session check on auth-related page:', router.pathname);\n                return; // Don't auto-check session on auth pages\n            }\n            // Auto-check session for other pages\n            const checkSession = {\n                \"App.useEffect.checkSession\": async ()=>{\n                    try {\n                        console.log('Auto-checking session for page:', router.pathname);\n                        await supabase.auth.getSession();\n                    } catch (error) {\n                        console.warn('Session check failed:', error);\n                    }\n                }\n            }[\"App.useEffect.checkSession\"];\n            checkSession();\n        }\n    }[\"App.useEffect\"], [\n        router.pathname,\n        supabase\n    ]);\n    return /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(SupabaseContext.Provider, {\n        value: {\n            supabase,\n            session: null,\n            user: null\n        },\n        children: /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(Component, {\n            ...pageProps\n        }, void 0, false, {\n            fileName: \"/Volumes/Work(SSD)/Personal Projects/codevision_app/codevision_app/frontend/pages/_app.tsx\",\n            lineNumber: 50,\n            columnNumber: 7\n        }, this)\n    }, void 0, false, {\n        fileName: \"/Volumes/Work(SSD)/Personal Projects/codevision_app/codevision_app/frontend/pages/_app.tsx\",\n        lineNumber: 49,\n        columnNumber: 5\n    }, this);\n}\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKHBhZ2VzLWRpci1ub2RlKS8uL3BhZ2VzL19hcHAudHN4IiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBCQUEwQjs7QUFDeUI7QUFFbUI7QUFFL0I7QUFDVDtBQUc5QixNQUFNTSxnQ0FBa0JMLG9EQUFhQSxDQUFrQ007QUFFaEUsU0FBU0M7SUFDZCxNQUFNQyxVQUFVUCxpREFBVUEsQ0FBQ0k7SUFDM0IsSUFBSSxDQUFDRyxTQUFTO1FBQ1osTUFBTSxJQUFJQyxNQUFNO0lBQ2xCO0lBQ0EsT0FBT0Q7QUFDVDtBQUVlLFNBQVNFLElBQUksRUFBRUMsU0FBUyxFQUFFQyxTQUFTLEVBQVk7SUFDNUQsTUFBTUMsU0FBU1Qsc0RBQVNBO0lBQ3hCLE1BQU0sQ0FBQ1UsU0FBUyxHQUFHWCwrQ0FBUUE7d0JBQWlCLElBQzFDSixrRUFBbUJBLENBQ2pCZ0IsMENBQW9DLEVBQ3BDQSxrTkFBeUM7O0lBSTdDLDREQUE0RDtJQUM1RGIsZ0RBQVNBO3lCQUFDO1lBQ1IsSUFBSVcsT0FBT00sUUFBUSxLQUFLLHFCQUFxQk4sT0FBT00sUUFBUSxLQUFLLGtCQUFrQjtnQkFDakZDLFFBQVFDLEdBQUcsQ0FBQyxxREFBcURSLE9BQU9NLFFBQVE7Z0JBQ2hGLFFBQU8seUNBQXlDO1lBQ2xEO1lBQ0EscUNBQXFDO1lBQ3JDLE1BQU1HOzhDQUFlO29CQUNuQixJQUFJO3dCQUNGRixRQUFRQyxHQUFHLENBQUMsbUNBQW1DUixPQUFPTSxRQUFRO3dCQUM5RCxNQUFNTCxTQUFTUyxJQUFJLENBQUNDLFVBQVU7b0JBQ2hDLEVBQUUsT0FBT0MsT0FBTzt3QkFDZEwsUUFBUU0sSUFBSSxDQUFDLHlCQUF5QkQ7b0JBQ3hDO2dCQUNGOztZQUVBSDtRQUNGO3dCQUFHO1FBQUNULE9BQU9NLFFBQVE7UUFBRUw7S0FBUztJQUU5QixxQkFDRSw4REFBQ1QsZ0JBQWdCc0IsUUFBUTtRQUFDQyxPQUFPO1lBQUVkO1lBQVVlLFNBQVM7WUFBTUMsTUFBTTtRQUFLO2tCQUNyRSw0RUFBQ25CO1lBQVcsR0FBR0MsU0FBUzs7Ozs7Ozs7Ozs7QUFHOUIiLCJzb3VyY2VzIjpbIi9Wb2x1bWVzL1dvcmsoU1NEKS9QZXJzb25hbCBQcm9qZWN0cy9jb2RldmlzaW9uX2FwcC9jb2RldmlzaW9uX2FwcC9mcm9udGVuZC9wYWdlcy9fYXBwLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBmcm9udGVuZC9wYWdlcy9fYXBwLnRzeFxuaW1wb3J0IHsgY3JlYXRlQnJvd3NlckNsaWVudCB9IGZyb20gJ0BzdXBhYmFzZS9zc3InXG5pbXBvcnQgdHlwZSB7IFN1cGFiYXNlQ2xpZW50IH0gZnJvbSAnQHN1cGFiYXNlL3N1cGFiYXNlLWpzJ1xuaW1wb3J0IHsgY3JlYXRlQ29udGV4dCwgdXNlQ29udGV4dCwgdXNlRWZmZWN0LCB1c2VTdGF0ZSB9IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHR5cGUgeyBBcHBQcm9wcyB9IGZyb20gJ25leHQvYXBwJ1xuaW1wb3J0IHsgdXNlUm91dGVyIH0gZnJvbSAnbmV4dC9yb3V0ZXInXG5pbXBvcnQgJy4uL3N0eWxlcy9nbG9iYWxzLmNzcydcbmltcG9ydCB7IFN1cGFiYXNlQ29udGV4dFR5cGUgfSBmcm9tICcuLi9saWIvdHlwZXMnXG5cbmNvbnN0IFN1cGFiYXNlQ29udGV4dCA9IGNyZWF0ZUNvbnRleHQ8U3VwYWJhc2VDb250ZXh0VHlwZSB8IHVuZGVmaW5lZD4odW5kZWZpbmVkKVxuXG5leHBvcnQgZnVuY3Rpb24gdXNlU3VwYWJhc2UoKTogU3VwYWJhc2VDb250ZXh0VHlwZSB7XG4gIGNvbnN0IGNvbnRleHQgPSB1c2VDb250ZXh0KFN1cGFiYXNlQ29udGV4dClcbiAgaWYgKCFjb250ZXh0KSB7XG4gICAgdGhyb3cgbmV3IEVycm9yKCd1c2VTdXBhYmFzZSBtdXN0IGJlIHVzZWQgd2l0aGluIGEgU3VwYWJhc2VQcm92aWRlcicpXG4gIH1cbiAgcmV0dXJuIGNvbnRleHRcbn1cblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gQXBwKHsgQ29tcG9uZW50LCBwYWdlUHJvcHMgfTogQXBwUHJvcHMpIHtcbiAgY29uc3Qgcm91dGVyID0gdXNlUm91dGVyKClcbiAgY29uc3QgW3N1cGFiYXNlXSA9IHVzZVN0YXRlPFN1cGFiYXNlQ2xpZW50PigoKSA9PlxuICAgIGNyZWF0ZUJyb3dzZXJDbGllbnQoXG4gICAgICBwcm9jZXNzLmVudi5ORVhUX1BVQkxJQ19TVVBBQkFTRV9VUkwhLFxuICAgICAgcHJvY2Vzcy5lbnYuTkVYVF9QVUJMSUNfU1VQQUJBU0VfQU5PTl9LRVkhXG4gICAgKVxuICApXG5cbiAgLy8gUHJldmVudCBhdXRvbWF0aWMgc2Vzc2lvbiBjaGVja2luZyBvbiByZXNldC1wYXNzd29yZCBwYWdlXG4gIHVzZUVmZmVjdCgoKSA9PiB7XG4gICAgaWYgKHJvdXRlci5wYXRobmFtZSA9PT0gJy9yZXNldC1wYXNzd29yZCcgfHwgcm91dGVyLnBhdGhuYW1lID09PSAnL2NvbmZpcm0tZW1haWwnKSB7XG4gICAgICBjb25zb2xlLmxvZygnU2tpcHBpbmcgYXV0byBzZXNzaW9uIGNoZWNrIG9uIGF1dGgtcmVsYXRlZCBwYWdlOicsIHJvdXRlci5wYXRobmFtZSlcbiAgICAgIHJldHVybiAvLyBEb24ndCBhdXRvLWNoZWNrIHNlc3Npb24gb24gYXV0aCBwYWdlc1xuICAgIH1cbiAgICAvLyBBdXRvLWNoZWNrIHNlc3Npb24gZm9yIG90aGVyIHBhZ2VzXG4gICAgY29uc3QgY2hlY2tTZXNzaW9uID0gYXN5bmMgKCkgPT4ge1xuICAgICAgdHJ5IHtcbiAgICAgICAgY29uc29sZS5sb2coJ0F1dG8tY2hlY2tpbmcgc2Vzc2lvbiBmb3IgcGFnZTonLCByb3V0ZXIucGF0aG5hbWUpXG4gICAgICAgIGF3YWl0IHN1cGFiYXNlLmF1dGguZ2V0U2Vzc2lvbigpXG4gICAgICB9IGNhdGNoIChlcnJvcikge1xuICAgICAgICBjb25zb2xlLndhcm4oJ1Nlc3Npb24gY2hlY2sgZmFpbGVkOicsIGVycm9yKVxuICAgICAgfVxuICAgIH1cblxuICAgIGNoZWNrU2Vzc2lvbigpXG4gIH0sIFtyb3V0ZXIucGF0aG5hbWUsIHN1cGFiYXNlXSlcblxuICByZXR1cm4gKFxuICAgIDxTdXBhYmFzZUNvbnRleHQuUHJvdmlkZXIgdmFsdWU9e3sgc3VwYWJhc2UsIHNlc3Npb246IG51bGwsIHVzZXI6IG51bGwgfX0+XG4gICAgICA8Q29tcG9uZW50IHsuLi5wYWdlUHJvcHN9IC8+XG4gICAgPC9TdXBhYmFzZUNvbnRleHQuUHJvdmlkZXI+XG4gIClcbn0iXSwibmFtZXMiOlsiY3JlYXRlQnJvd3NlckNsaWVudCIsImNyZWF0ZUNvbnRleHQiLCJ1c2VDb250ZXh0IiwidXNlRWZmZWN0IiwidXNlU3RhdGUiLCJ1c2VSb3V0ZXIiLCJTdXBhYmFzZUNvbnRleHQiLCJ1bmRlZmluZWQiLCJ1c2VTdXBhYmFzZSIsImNvbnRleHQiLCJFcnJvciIsIkFwcCIsIkNvbXBvbmVudCIsInBhZ2VQcm9wcyIsInJvdXRlciIsInN1cGFiYXNlIiwicHJvY2VzcyIsImVudiIsIk5FWFRfUFVCTElDX1NVUEFCQVNFX1VSTCIsIk5FWFRfUFVCTElDX1NVUEFCQVNFX0FOT05fS0VZIiwicGF0aG5hbWUiLCJjb25zb2xlIiwibG9nIiwiY2hlY2tTZXNzaW9uIiwiYXV0aCIsImdldFNlc3Npb24iLCJlcnJvciIsIndhcm4iLCJQcm92aWRlciIsInZhbHVlIiwic2Vzc2lvbiIsInVzZXIiXSwiaWdub3JlTGlzdCI6W10sInNvdXJjZVJvb3QiOiIifQ==\n//# sourceURL=webpack-internal:///(pages-dir-node)/./pages/_app.tsx\n");

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