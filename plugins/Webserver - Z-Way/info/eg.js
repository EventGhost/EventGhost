//Plugin for z-way server to connect to EventGhost "Webserver - Z-Way" plugin v0.40.1

var EGcomClasses={};
function EGcom(){
  return new function(){
    this.login="";
    this.password="";
    this.url="";
    this.alias="undefined";
    this.monitoredDevices=[];
    this.EGserverOn=true;
    this.bindFunctions={};

    this.bindF = function(id,unit,parameter){
      unit=unit||"State";
      var alias=this.alias;
      this.bindFunctions[JSON.stringify(id)]=function(){
        if(EGcomClasses[alias].EGserverOn){
          var nr=id[0];
          var inst=id[1];
          var comClass=id[2];
          var typeName=zway.devices[nr].instances[inst].commandClasses[comClass].name;
          try{
            var id2=id.slice();
            id2.pop();
            var tempData=JSON.stringify({"method":"TriggerEvent","kwargs":{"prefix":"Z-Way","suffix":alias,"payload":[typeName,id2,this.value,unit]}});
            if (parameter){
              tempData=JSON.stringify({"method":"TriggerEvent","kwargs":{"prefix":"Z-Way","suffix":alias,"payload":[typeName,id2,this.value,unit,parameter]}});
            }
            http.request({
              url: EGcomClasses[alias].url,
              method: "POST",
              auth: {
                login: EGcomClasses[alias].login,
                password: EGcomClasses[alias].password
              },
              async: true,
              data: tempData
            });
            if (comClass=="51" && (id[3]=="2" || id[3]=="3" || id[3]=="4")){
              var tmpVal=this.value.toString(16).toUpperCase();
              while (tmpVal.length<2){
                tmpVal="0"+tmpVal;
              }
              EGcomClasses[alias].deviceData[JSON.stringify([id[0],id[1],id[2]])][id[3]]=tmpVal;
              http.request({
                url: EGcomClasses[alias].url,
                method: "POST",
                auth: {
                  login: EGcomClasses[alias].login,
                  password: EGcomClasses[alias].password
                },
                async: true,
                data: JSON.stringify({"method":"TriggerEvent","kwargs":{"prefix":"Z-Way","suffix":alias,"payload":[typeName,[id[0],id[1],id[2]],"#"+EGcomClasses[alias].deviceData[JSON.stringify([id[0],id[1],id[2]])]["2"]+EGcomClasses[alias].deviceData[JSON.stringify([id[0],id[1],id[2]])]["3"]+EGcomClasses[alias].deviceData[JSON.stringify([id[0],id[1],id[2]])]["4"],"RGB"]}})
              });
            }
          }
          catch(e){
            EGcomClasses[alias].EGserverOn=false;
          }
        }
      };
      return this.bindFunctions[JSON.stringify(id)];
    }

    this.okF = function(id){
      this.monitoredDevices.push(id);
    }

    this.getAllStates = function(){
      for (var i=0; i<this.monitoredDevices.length; i++){
        if (this.monitoredDevices[i][2]=="51"){
          for (var mode in this.monitoredDevices[i][3]){
            zway.devices[this.monitoredDevices[i][0]].instances[this.monitoredDevices[i][1]].commandClasses[this.monitoredDevices[i][2]].Get(mode);
          }
        }
        else{
          zway.devices[this.monitoredDevices[i][0]].instances[this.monitoredDevices[i][1]].commandClasses[this.monitoredDevices[i][2]].Get();
        }
      }
    }
    
    this.print =function(text){
      http.request({
        url: this.url,
        method: "POST",
        auth: {
          login: this.login,
          password: this.password
        },
        async: true,
        data: JSON.stringify({"method":"TriggerEvent","kwargs":{"prefix":"Z-Way","suffix":"Debug."+this.alias,"payload":text}})
      });
    }
    
    this.initiateDevices = function (initNew,deleteOld){
      this.monitoredDevices=[];
      for (var nr in zway.devices){
        if (nr!=1){
          for (var inst in zway.devices[nr].instances){
            for (var comClass in zway.devices[nr].instances[inst].commandClasses){
              try{
                if(comClass==37){
                  if (deleteOld){
                    try{
                      zway.devices[nr].instances[inst].commandClasses[comClass].data.level.unbind(this.bindFunctions[JSON.stringify([nr,inst,comClass,0])]);
                    }
                    catch(e){
                      this.print(nr+inst+comClass);
                    }
                  }
                  if (initNew){
                    zway.devices[nr].instances[inst].commandClasses[comClass].data.level.bind(this.bindF([nr,inst,comClass,0]));
                    this.okF([nr,inst,comClass]);
                  }
                }
                else if(comClass==38){
                  if (deleteOld){
                    try{
                      zway.devices[nr].instances[inst].commandClasses[comClass].data.level.unbind(this.bindFunctions[JSON.stringify([nr,inst,comClass,0])]);
                    }
                    catch(e){
                      this.print(nr+inst+comClass);
                    }
                  }
                  if (initNew){
                    zway.devices[nr].instances[inst].commandClasses[comClass].data.level.bind(this.bindF([nr,inst,comClass,0],'%'));
                    this.okF([nr,inst,comClass]);
                  }
                }
                else if(comClass==48){
                  for (var mode in zway.devices[nr].instances[inst].commandClasses[comClass].data){
                    if (!isNaN(parseFloat(mode)) && isFinite(mode)){
                      if (deleteOld){
                        try{
                          zway.devices[nr].instances[inst].commandClasses[comClass].data[mode].level.unbind(this.bindFunctions[JSON.stringify([nr,inst,comClass,mode,0])]);
                        }
                        catch(e){
                          this.print(nr+inst+comClass+mode);
                        }
                      }
                      if (initNew){
                        zway.devices[nr].instances[inst].commandClasses[comClass].data[mode].level.bind(this.bindF([nr,inst,comClass,mode,0]));
                        this.okF([nr,inst,comClass,mode]);
                      }
                    }
                  }
                }
                else if(comClass==49 || comClass==50){
                  for (var mode in zway.devices[nr].instances[inst].commandClasses[comClass].data){
                    if (!isNaN(parseFloat(mode)) && isFinite(mode)){
                      if (deleteOld){
                        try{
                          zway.devices[nr].instances[inst].commandClasses[comClass].data[mode].val.unbind(this.bindFunctions[JSON.stringify([nr,inst,comClass,mode,0])]);
                        }
                        catch(e){
                          this.print(nr+inst+comClass+mode);
                        }
                      }
                      if (initNew){
                        zway.devices[nr].instances[inst].commandClasses[comClass].data[mode].val.bind(this.bindF([nr,inst,comClass,mode,0],zway.devices[nr].instances[inst].commandClasses[comClass].data[mode].scaleString.value));
                        this.okF([nr,inst,comClass,mode]);
                      }
                    }
                  }
                }
                else if(comClass==67){
                  for (var mode in zway.devices[nr].instances[inst].commandClasses[comClass].data){
                    if (!isNaN(parseFloat(mode)) && isFinite(mode)){
                      if (deleteOld){
                        try{
                          zway.devices[nr].instances[inst].commandClasses[comClass].data[mode].val.unbind(this.bindFunctions[JSON.stringify([nr,inst,comClass,mode,0])]);
                          zway.devices[nr].instances[inst].commandClasses[comClass].data[mode].setVal.unbind(this.bindFunctions[JSON.stringify([nr,inst,comClass,mode,1])]);
                        }
                        catch(e){
                          this.print(nr+inst+comClass+mode);
                        }
                      }
                      if (initNew){
                        zway.devices[nr].instances[inst].commandClasses[comClass].data[mode].val.bind(this.bindF([nr,inst,comClass,mode,0],zway.devices[nr].instances[inst].commandClasses[comClass].data[mode].scaleString.value,'val'));
                        zway.devices[nr].instances[inst].commandClasses[comClass].data[mode].setVal.bind(this.bindF([nr,inst,comClass,mode,1],zway.devices[nr].instances[inst].commandClasses[comClass].data[mode].scaleString.value,'setVal'));
                        this.okF([nr,inst,comClass,mode]);
                      }
                    }
                  }
                }
                else if(comClass==64){
                  if (deleteOld){
                    try{
                      zway.devices[nr].instances[inst].commandClasses[comClass].data['mode'].unbind(this.bindFunctions[JSON.stringify([nr,inst,comClass,0])]);
                    }
                    catch(e){
                      this.print(nr+inst+comClass);
                    }
                  }
                  if (initNew){
                    zway.devices[nr].instances[inst].commandClasses[comClass].data['mode'].bind(this.bindF([nr,inst,comClass,0],'mode'));
                  }
                  for (var mode in zway.devices[nr].instances[inst].commandClasses[comClass].data){
                    if (!isNaN(parseFloat(mode)) && isFinite(mode)){
                      if (initNew){
                        this.okF([nr,inst,comClass,mode]);
                      }
                    }
                  }
                }
                else if(comClass==51){
                  this.deviceData[JSON.stringify([nr,inst,comClass])]={};
                  for (var mode in zway.devices[nr].instances[inst].commandClasses[comClass].data){
                    if (!isNaN(parseFloat(mode)) && isFinite(mode)){
                      if (deleteOld){
                        try{
                          zway.devices[nr].instances[inst].commandClasses[comClass].data[mode].level.unbind(this.bindFunctions[JSON.stringify([nr,inst,comClass,mode,0])]);
                        }
                        catch(e){
                          this.print(nr+inst+comClass+mode);
                        }
                      }
                      if (initNew){
                        var tmpVal=zway.devices[nr].instances[inst].commandClasses[comClass].data[mode].level.value.toString(16).toUpperCase();
                        while (tmpVal.length<2){
                          tmpVal="0"+tmpVal;
                        }
                        this.deviceData[JSON.stringify([nr,inst,comClass])][mode]=tmpVal;
                        zway.devices[nr].instances[inst].commandClasses[comClass].data[mode].level.bind(this.bindF([nr,inst,comClass,mode,0],zway.devices[nr].instances[inst].commandClasses[comClass].data[mode].capabilityString.value));
                        this.okF([nr,inst,comClass,mode]);
                      }
                    }
                  }
                }
                else{
                  continue;
                }
              }
              catch(e){
                if(this.EGserverOn){
                  try{
                    http.request({
                      url: this.url,
                      method: "POST",
                      auth: {
                        login: this.login,
                        password: this.password
                      },
                      async: true,
                      data: JSON.stringify({"method":"TriggerEvent","kwargs":{"prefix":"Z-Way","suffix":"Error."+this.alias,"payload":[nr,inst,comClass]}})
                    });
                  }
                  catch(e){
                    this.EGserverOn=false;
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}

function initEG(data){
  data=JSON.parse(decodeURIComponent(data));
  if (typeof EGcomClasses[data[0]]=="undefined"){
    EGcomClasses[data[0]]=EGcom();
    EGcomClasses[data[0]].deviceData={}
  }
  EGcomClasses[data[0]].EGserverOn=true;
  var targetPort=data[2];
  var targetFile=data[3].replace(/~fs~/g,"/").replace(/~bs~/g,"/");
  var targetProtocol=data[6];
  EGcomClasses[data[0]].login=data[4];
  EGcomClasses[data[0]].password=data[5];
  EGcomClasses[data[0]].alias=data[0];
  for (var i=0; i<data[1].length; i++){
      EGcomClasses[data[0]].url=targetProtocol+"://"+data[1][i]+":"+targetPort+targetFile;
      try{
          EGcomClasses[data[0]].print("connected!");
          break;
      }
      catch(e){
          continue;
      }
  }
  EGcomClasses[data[0]].initiateDevices(true,true);
	return EGcomClasses[data[0]].monitoredDevices;
}

function getAllStates(alias){
  if (typeof EGcomClasses[alias]!="undefined"){
    EGcomClasses[alias].getAllStates();
  }
}

function removeHost(alias){
  if (typeof EGcomClasses[alias]!="undefined"){
    EGcomClasses[alias].initiateDevices(false,true);
    delete EGcomClasses[alias];
    return true;
  }
  delete EGcomClasses[alias];
  return false;
}