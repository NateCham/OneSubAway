GeoLocation = Backbone.Model.extend({
  getGeo: function() {
    var promise = $.Deferred();

    navigator.geolocation.getCurrentPosition(function() {
      var p = arguments[0];
      promise.resolve([p.coords.latitude, p.coords.longitude]);
    });
    return promise;
  }
});

StopModel = Backbone.Model.extend({});

StopsCollection = Backbone.Collection.extend({
  model: StopModel,
  parse: function(data) { 
    //console.log(data);
    return data.stations; 
  },
  initialize: function(models, options) {
    this.station = options.station;
  }
});

StationModel = Backbone.Model.extend({});

StationsCollection = Backbone.Collection.extend({
  model: StationModel,
  url: function() {
    return '/nearest?latitude=' + this.lat + '&longitude=' + this.lon;
    //return '/nearest?latitude=' + '40.869444' + '&longitude=' + '-73.915279';
  },
  parse: function(data) { return data.nearest; },
  initialize: function() {
    var self = this;
    this.geoLocation = (new GeoLocation()).getGeo().then(function(location) {
      self.lat = location[0];
      self.lon = location[1];
      $.when(self.fetch()).then(function() {
        self.getStops();
      });
    });
  },
  getStops: function() {
    //console.log(this);
    this.each(function ( station ) {
      station.stops = new StopsCollection([], { station: station });
      station.stops.url = '/stop/' + station.attributes.stop_id;
      $.when(station.stops.fetch()).then(function() {
        //console.log(station.stops);
      });
    });
    StationsApp.mainRegion.show(stationsView);
    
  }
});

StationsApp = new Backbone.Marionette.Application();

StationsApp.addRegions({
  mainRegion: '#stations-app'
});

StopView = Backbone.Marionette.CompositeView.extend({
  template: '#train-item-tmpl',
  tagName: 'li',
  initialize: function() {
    console.log(this);
  }

});

StationView = Backbone.Marionette.CompositeView.extend({
  template: '#nearest-item-tmpl',
  className: 'station',
  childView: StopView,
  initialize: function() {
    this.collection = this.model.stops;
  }
});

StationsView = Backbone.Marionette.CollectionView.extend({
  id: 'stationList',
  className: 'stations',
  childView: StationView
});



/*
var StopsListItemView = Backbone.View.extend({
  tagName: 'div',
  className: 'stop',
  template: _.template($('#train-item-tmpl').html()),
  render: function() {
    var html = this.template(this.model.toJSON());
    this.$el.html(html);
    return this;
  }
});

var StopsListView = Backbone.View.extend({
  el: '#stop',
  initialize: function() {
    this.listenTo(this.collection, 'sync', this.render);
  },
  render: function() {
    var $list = this.$('div.stops-list').empty();
    
    this.collection.each(function(model) {
      var item = new StopsListItemView({model: model});
      $list.append(item.render().$el);
    }, this);

    return this;
  }
});

var StationsListItemView = Backbone.View.extend({
  tagName: 'div',
  className: 'nearest',
  template: _.template($('#nearest-item-tmpl').html()),

  render: function() {
    var html = this.template(this.model.toJSON());
    this.$el.html(html);
    console.log(this);
    return this;
  }
});

var StationsListView = Backbone.View.extend({
  el: '#stations-app',
  initialize: function() {
    this.listenTo(this.collection, 'sync', this.render);
  },
  render: function() {
    var $list = this.$('div.stations-list').empty();
    this.collection.each(function(model) {
      var item = new StationsListItemView({model: model});
      $list.append(item.render().$el);
    }, this);
    return this;
  }
});

var stationsList = new StationsCollection();
var stationsView = new StationsListView({collection: stationsList});

*/

var stationsList = new StationsCollection();
var stationsView = new StationsView({collection: stationsList });
