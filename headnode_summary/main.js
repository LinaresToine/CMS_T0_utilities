
var currentTime = "";
//by default, hide the replays content:
$( "#replayContent" ).hide();
$( "#testbedDown" ).hide();

var jsonData = $.getJSON( "data.json", function( data ) {
  var items = [];
  $.each( data, function( key, val ) {
    var configFile = "";
    var nodeStatus = "";
    var acqEra = "";
    var minRun = "";
    var maxRun = "";
    var cmssw = "";
    var t0Version = "";
    var scenario = "";
    var processingVersion = "";
    var jobpaused = 0;
    var jobRunning = 0;
    var jobIdle = 0;
    var success = 0;
    var complete = 0;
    var created = 0;
    var executing = 0;
    var cleanout = 0;
    var downComponents = "";
    var t0astInst = "";
    var recoDelay = " ";

    currentTime = data[key]["update time"];
    items.push( "<tr>" );
    if (typeof data[key]["T0AST"] !== 'undefined'){
        t0astInst = data[key]["T0AST"]
    }
    if (typeof data[key]["Configuration"] !== 'undefined'){
        configFile = data[key]["Configuration"]
    }
    if (typeof data[key]["status"] !== 'undefined'){
        nodeStatus = data[key]["status"]
    } 
    if (typeof data[key]["AcquisitionEra"] !== 'undefined'){
        acqEra = data[key]["AcquisitionEra"]
    } 
    if (typeof data[key]["MinRun"] !== 'undefined'){
        minRun = data[key]["MinRun"]
    } 
    if (typeof data[key]["MaxRun"] !== 'undefined'){
        maxRun = data[key]["MaxRun"]
    } 
    if (typeof data[key]["CMSSWVersion"] !== 'undefined'){
        cmssw = data[key]["CMSSWVersion"]
    } 
    if (typeof data[key]["tier0Version"] !== 'undefined'){
        t0Version = data[key]["tier0Version"]
    } 
    if (typeof data[key]["Scenario"] !== 'undefined'){
        scenario = data[key]["Scenario"]
    }
    if (typeof data[key]["ProcessingVersion"] !== 'undefined'){
      processingVersion = data[key]["ProcessingVersion"]
    }
    if (typeof data[key]["created"] !== 'undefined'){
        created = data[key]["created"]
    }
    if (typeof data[key]["executing"] !== 'undefined'){
        executing = data[key]["executing"]
    }
    if (typeof data[key]["running"] !== 'undefined'){
        jobRunning = data[key]["running"]
    }
    if (typeof data[key]["idle"] !== 'undefined'){
        jobIdle = data[key]["idle"]
    }
    if (typeof data[key]["success"] !== 'undefined'){
        success = data[key]["success"]
    }
    if (typeof data[key]["complete"] !== 'undefined'){
        complete = data[key]["complete"]
    }
    if (typeof data[key]["cleanout"] !== 'undefined'){
        cleanout = data[key]["cleanout"]
    }
    if (typeof data[key]["paused"] !== 'undefined'){
        jobpaused = data[key]["paused"]
    }
    if (typeof data[key]["components down"] !== 'undefined'){
        downComponents = data[key]["components down"]
        downComponents = downComponents.toString().replace(/\,/g, "\n")
    }
    if (typeof data[key]["RecoDelay"] !== 'undefined'){
        recoDelay = data[key]["RecoDelay"]
    }

    items.push( "<td><p><a href='" + configFile + "'>" + key  + "</a></p></td>" );
    if (nodeStatus !== 'ok') {
      items.push( "<td><p class=\"red\">" + nodeStatus + "</p></td>" );
    } else {
      items.push( "<td><p>" + nodeStatus + "</p></td>" );
    }
    items.push( "<td><p>" + acqEra + "</p></td>" )
    items.push( "<td><p>" + minRun + "</p></td>" );
    items.push( "<td><p>" + maxRun + "</p></td>" );
    items.push( "<td><p>" + cmssw + "</p></td>" );
    items.push( "<td><p>" + t0Version + "</p></td>" );
    items.push( "<td><p>" + scenario + "</p></td>" );
    items.push( "<td><p>" + processingVersion + "</p></td>" );
    items.push( "<td><p>" + recoDelay + "</p></td>" );
    items.push( "<td><p>" + created + "</p></td>" );
    items.push( "<td><p>" + executing + "</p></td>" );
    items.push( "<td><p>" + jobRunning + "</p></td>" );
    items.push( "<td><p>" + jobIdle + "</p></td>" );
    items.push( "<td><p>" + success + "</p></td>" );
    items.push( "<td><p>" + complete + "</p></td>" );
    items.push( "<td><p>" + cleanout + "</p></td>" );
    if (jobpaused !== 0 ) {
      items.push( "<td><p class=\"red\">" + jobpaused + "</p></td>" );
    } else {
      items.push( "<td><p>" + jobpaused + "</p></td>" );
    }
    items.push( "<td><p>" + downComponents + "</p></td>" );
    items.push( "<td><p>" + t0astInst + "</p></td>" );
    items.push( "</tr>" );
  });
 
  $( "#summaryTableBody" ).append(items);
  $( "#lastReportTime" ).append( "Production nodes. Last report time: "+ currentTime );
});


var jsonReplayData = $.getJSON( "dataReplay.json", function( data ) {
  if (!jQuery.isEmptyObject(data)) {
    $( "#replayContent" ).show();
    var items = [];

    $.each( data, function( key, val ) {
      var configFile = "";
      var nodeStatus = "";
      var injectedRuns = "";
      var cmssw = "";
      var t0Version = "";
      var scenario = "";
      var jobpaused = 0;
      var jobRunning = 0;
      var jobIdle = 0;
      var success = 0;
      var complete = 0;
      var created = 0;
      var executing = 0;
      var cleanout = 0;
      var downComponents = "";
      var t0astInst = "";
      items.push( "<tr>" );
      if (typeof data[key]["Configuration"] !== 'undefined'){
        configFile = data[key]["Configuration"]
      }
      if (typeof data[key]["T0AST"] !== 'undefined'){
        t0astInst = data[key]["T0AST"]
      }
      if (typeof data[key]["status"] !== 'undefined'){
        nodeStatus = data[key]["status"]
      }
      if (typeof data[key]["Runs"] !== 'undefined'){
        injectedRuns = data[key]["Runs"]
      }
      if (typeof data[key]["CMSSWVersion"] !== 'undefined'){
        cmssw = data[key]["CMSSWVersion"]
      }
      if (typeof data[key]["tier0Version"] !== 'undefined'){
         t0Version = data[key]["tier0Version"]
      }
      if (typeof data[key]["Scenario"] !== 'undefined'){
        scenario = data[key]["Scenario"]
      }
      if (typeof data[key]["paused"] !== 'undefined'){
        jobpaused = data[key]["paused"]
      }
      if (typeof data[key]["running"] !== 'undefined'){
        jobRunning = data[key]["running"]
      }
      if (typeof data[key]["idle"] !== 'undefined'){
        jobIdle = data[key]["idle"]
      }
      if (typeof data[key]["success"] !== 'undefined'){
        success = data[key]["success"]
      }
      if (typeof data[key]["complete"] !== 'undefined'){
        complete = data[key]["complete"]
      }
      if (typeof data[key]["created"] !== 'undefined'){
        created = data[key]["created"]
      }
      if (typeof data[key]["executing"] !== 'undefined'){
        executing = data[key]["executing"]
      }
      if (typeof data[key]["cleanout"] !== 'undefined'){
        cleanout = data[key]["cleanout"]
      }
      if (typeof data[key]["components down"] !== 'undefined'){
        downComponents = data[key]["components down"]
        downComponents = downComponents.toString().replace(/\,/g, "\n")
      }

      items.push( "<tr>" );
      items.push( "<td><p><a href='" + configFile + "'>" + key  + "</a></p></td>" );
      if ( nodeStatus !== 'ok') {
        items.push( "<td><p class=\"red\">" + nodeStatus + "</p></td>" );
      } else {
        items.push( "<td><p>" + nodeStatus + "</p></td>" );
      }      
      items.push( "<td><p>" + injectedRuns + "</p></td>" );
      items.push( "<td><p>" + cmssw + "</p></td>" );
      items.push( "<td><p>" + t0Version + "</p></td>" );
      items.push( "<td><p>" + scenario + "</p></td>" );
      items.push( "<td><p>" + created + "</p></td>" );
      items.push( "<td><p>" + executing + "</p></td>" );
      items.push( "<td><p>" + jobRunning + "</p></td>" );
      items.push( "<td><p>" + jobIdle + "</p></td>" );
      items.push( "<td><p>" + success + "</p></td>" );
      items.push( "<td><p>" + complete + "</p></td>" );
      items.push( "<td><p>" + cleanout + "</p></td>" );
      if (jobpaused !== 0 ) {
        items.push( "<td><p class=\"red\">" + jobpaused + "</p></td>" );
      } else {
        items.push( "<td><p>" + jobpaused + "</p></td>" );
      }
      items.push( "<td><p>" + downComponents + "</p></td>" );
      items.push( "<td><p><a href='" + data[key]["monitoringUrl"] + "'>" + "link"  + "</a></p></td>" );
      items.push( "<td><p>" + t0astInst + "</p></td>" );
      items.push( "</tr>" );
    });
  
    $( "#summaryTableBodyReplay" ).append(items);
  }
  else {
   $( "#testbedDown" ).show(); 
  }
});



