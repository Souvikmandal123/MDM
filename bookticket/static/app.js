var app = angular.module('AuthApp', ['ngRoute']);

app.config(function($routeProvider){
  $routeProvider
    .when('/register', { templateUrl: '/static/tpl/register.html', controller: 'RegisterCtrl' })
    .when('/verify-register', { templateUrl: '/static/tpl/verify-register.html', controller: 'VerifyRegisterCtrl' })
    .when('/login', { templateUrl: '/static/tpl/login.html', controller: 'LoginCtrl' })
    .when('/login/verify', { templateUrl: '/static/tpl/login-verify.html', controller: 'LoginVerifyCtrl' })
    .otherwise({ redirectTo: '/login' });
});

app.factory('Api', function($http){
  const base = '/api/';
  return {
    register: (data) => $http.post(base + 'register/', data),
    verifyRegister: (data) => $http.post(base + 'verify-register-otp/', data),
    loginStart: (data) => $http.post(base + 'login/', data),
    loginVerify: (data) => $http.post(base + 'login/verify/', data),
  };
});

app.controller('RegisterCtrl', function($scope, $location, Api){
  $scope.data = {};
  $scope.msg = null;
  $scope.submit = function(){
    Api.register($scope.data).then(res=>{
      $scope.msg = res.data.detail;
      sessionStorage.setItem('email', $scope.data.email);
      $location.path('/verify-register');
    }, err=>{
      $scope.msg = JSON.stringify(err.data);
    });
  };
});

app.controller('VerifyRegisterCtrl', function($scope, $location, Api){
  $scope.data = { email: sessionStorage.getItem('email') || '' };
  $scope.msg = null;
  $scope.submit = function(){
    Api.verifyRegister($scope.data).then(res=>{
      $scope.msg = res.data.detail;
      $location.path('/login');
    }, err=>{
      $scope.msg = err.data.detail || 'Error';
    });
  };
});

app.controller('LoginCtrl', function($scope, $location, Api){
  $scope.data = {};
  $scope.msg = null;
  $scope.submit = function(){
    Api.loginStart($scope.data).then(res=>{
      $scope.msg = res.data.detail;
      sessionStorage.setItem('email', $scope.data.email);
      $location.path('/login/verify');
    }, err=>{
      $scope.msg = err.data.detail || 'Error';
    });
  };
});

app.controller('LoginVerifyCtrl', function($scope, $location, Api){
  $scope.data = { email: sessionStorage.getItem('email') || '' };
  $scope.msg = null;
  $scope.submit = function(){
    Api.loginVerify($scope.data).then(res=>{
      $scope.msg = res.data.detail;
      localStorage.setItem('access', res.data.tokens.access);
      localStorage.setItem('refresh', res.data.tokens.refresh);
      alert('Logged in successfully!');
      $location.path('/login');
    }, err=>{
      $scope.msg = err.data.detail || 'Error';
    });
  };
});
