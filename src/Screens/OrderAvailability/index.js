/* eslint-disable react-native/no-inline-styles */
import React, {useEffect, useState} from 'react';
import {View, Text, ScrollView} from 'react-native';
import LoadingActionContainer from '../../Components/LoadingActionContainer';
import {Container, HeaderButton, InputX} from '../../Components';
import useAppTheme from '../../Themes/Context';
import {IconX, ICON_TYPE} from '../../Icons';
import {useStoreState} from 'easy-peasy';
import Fonts from '../../Themes/Fonts';
import {TouchableOpacity, ListItem} from 'react-native';
import AudioRecord from 'react-native-audio-record';
import {BASE_URL} from '../../Config/index';
import Tts from 'react-native-tts';
import {ButtonX} from '../../Components';
import { Avatar, Button, Card, Title, Paragraph } from 'react-native-paper';
import AsyncStorage from '@react-native-community/async-storage';
import { Voice } from '@react-native-voice/voice';

const MainScreen = ({routes, route, navigation}) => {
  const {theme} = useAppTheme();
  // eslint-disable-next-line prettier/prettier
  const {username, password} = useStoreState((state) => ({
    username: state.login.username,
    password: state.login.password,
  }));
  const [resData, setResData] = useState('');
  const [language, setLanguage] = useState('en');
  const [languageTts, setLanguageTts] = useState('en-IN');
  const [availability, setAvailability] = useState([]);
  const [pharmaceutical, setPharmaceutical] = useState([]);
  const [prescription, setPrescription] = useState([]);
  const [searchItems, setSearchItems] = useState(route.params);
  const [isRecording, setIsRecording] = useState(false);

  const LISTEN_COMMAND_EN = "begin"
  const LISTEN_COMMAND_TA = "தொடங்க"

  const {
    translations
  } = useContext(LocalizationContext);

  useEffect(() => {
    Voice.onSpeechStart = onSpeechStart()
    Voice.onSpeechRecognized = onSpeechRecognized()
    Voice.onSpeechResults = onSpeechResults()

    var allAvailability=[]
    for (var i = 0; i < searchItems.length; i++) {
      if (searchItems[i].perc > 0) {
        // Only Consider Shops with percentage Greater than 0
        var items = []
        var similaritems=[]

        // Store Items
        for(var j=0; j < searchItems[i].shopObj.items.length; j++) {
          items.push(searchItems[i].shopObj.items[j])
        }

        // Store Similar Items
        for (var j=0; j < searchItems[i].shopObj.similaritems.length; j++) {
          similaritems.push(searchItems[i].shopObj.similaritems[j])
        }

        allAvailability.push({"shop_id":searchItems[i].shopObj._id, "availability": searchItems[i].perc, "shop_name": searchItems[i].shopObj.shop_name, "shop_address": searchItems[i].shopObj.shop_address, "shop_lat": searchItems[i].shopObj.shop_lat, "shop_long": searchItems[i].shopObj.shop_long, "items": items, "similarItems":similaritems})
      }
    }

    // Set Shop Availability
    setAvailability(allAvailability)
    // availability.push({"shop_id":1,"shop_name":"Taniya","shop_address":"Main Road, Colombo","availability":0.75})
    // availability.push({"shop_id":2,"shop_name":"Wijesekara","shop_address":"Main Road, Colombo","availability":0.25})
    var msg = "";

    for (var i=0; i < availability.length; i++) {
      msg += "Shop "+availability[i].shop_name+" has an availability of "+(availability[i].perc)+"% of the total list"
    }

    if (msg == "" || availability.length == 0) {
      msg = "The items you chose are not available in any shop yet!"
    }

    // Load the Chosen Language
    setLanguage(AsyncStorage.getItem('language'))

    if (language == 'ta') {
      setLanguageTts('ta-IN')
    } else {
      setLanguageTts('en-IN')
    }

    Tts.setDefaultLanguage(languageTts)
    Tts.speak('Availaibility of the Products that you are looking for based on the shops near you are as follows.\n'+msg, {
      androidParams: {
        KEY_PARAM_PAN: -1,
        KEY_PARAM_VOLUME: 0.5,
        KEY_PARAM_STREAM: 'STREAM_MUSIC',
      },
    });


    const _toggleDrawer = () => {
      navigation.toggleDrawer();
    };

    Tts.speak(
      'Your Product Availability has been checked against multiple Shops.',
      {
        androidParams: {
          KEY_PARAM_PAN: -1,
          KEY_PARAM_VOLUME: 0.5,
          KEY_PARAM_STREAM: 'STREAM_MUSIC',
        },
      },
    );
    const options = {
      sampleRate: 16000, // default 44100
      channels: 1, // 1 or 2, default 1
      bitsPerSample: 16, // 8 or 16, default 16
      audioSource: 6, // android only (see below)
      wavFile: 'test.wav', // default 'audio.wav'
    };

    AudioRecord.init(options);
    const interval = setInterval(() => {
      if (!isRecording) {
        // Not Recording username or password
        Voice.stop() // Stop Recording
        Voice.start(locale) // Start Recording Again
      }
    }, 5000);
  
    return () => clearInterval(interval); // This represents the unmount function, in which you need to clear your interval to prevent memory leaks.
  }, [navigation, theme.colors.headerTitle]);

  const onSpeechStart = (e) => {

  }

  const onSpeechRecognized = (e) => {
    
  }

  const onSpeechResults = (e) => {
    if (isRecording == false) {
      if (e.value.includes(LISTEN_COMMAND_EN) || e.value.includes(LISTEN_COMMAND_TA)) {
        setIsRecording(true)
        Voice.start(locale)
      }
    } else {
      // Read the Voice Result
      console.log(e.value)
      var menuitem = e.value;
      if (menuitem.includes("read") || menuitem.includes("படி")) {
        // Read the Availability

      } else if (menuitem.includes("shop")) {
        var list = menuitem.split("shop")
        if (list.length > 1 && list[1] != "") {
          // Shop ID
          var shop_id = list[1]
          for (var i=0; i < availability.length; i++) {
            if (availability[i].shop_id == shop_id) {
              selectShop(shop_id)
            }
          }
        }
      } else if (menuitem.includes("கடை")) {
        var list = menuitem.split("கடை")
        if (list.length > 1 && list[1] != "") {
          // Shop ID
          var shop_id = list[1]
          for (var i=0; i < availability.length; i++) {
            if (availability[i].shop_id == shop_id) {
              selectShop(shop_id)
            }
          }
        }
      } else if (menuitem.includes("go back") || menuitem.includes("திரும்பி செல்")) {
        navigation.navigate('language-success');
      }

      setIsRecording(false)
    }
  }

  const record = () => {
    console.log('record');

    AudioRecord.start();
    timeout;
    let timeout = setTimeout(() => {
      stopRecord();
      console.log('hello');
    }, 12000);
  };

  const stopRecord = async () => {
    console.log('recordStop ');
    const audioFile = await AudioRecord.stop();
    AudioRecord.on('data', (data) => {});
    console.log('audioFile 🍷', audioFile);
    initialRec(audioFile);
    // AudioRecord.stop();
  };

  const initialRec = (audioFile) => {
    uploadAudio(audioFile);
    console.log('initialRec', audioFile);
    const options = {
      sampleRate: 16000, // default 44100
      channels: 1, // 1 or 2, default 1
      bitsPerSample: 16, // 8 or 16, default 16
      audioSource: 6, // android only (see below)
      wavFile: 'test.wav', // default 'audio.wav'
    };
  };

  const uploadAudio = async (fileUrl) => {
    console.log('upload');
    console.log('🧑‍🚀🧑‍🚀', fileUrl);
    let formData = new FormData();
    formData.append('audioFile', {
      uri: 'file:///data/user/0/com.easy_boiler/files/test.wav',
      type: 'audio/wav',
      name: 'test.wav',
    });
    formData.append('userId', 3);

    fetch(`${BASE_URL}/voicesearch/en`, {
      method: 'POST',
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((response) => {
        console.log('response 🔥', response.flag);
        console.log(response);

        if (response.flag == 'back') {
          navigation.navigate('language-success');
        }
        if (response.flag == 'place-order') {
          navigation.navigate('place-order', {
            response,
          });
        }
        if (response.flag == 'search-save') {
          navigation.navigate('search-save', {
            response,
          });
        }
        if (response.flag == 'check-order') {
          navigation.navigate('check-order');
        }
        if (response.flag == 'checkout') {
          Tts.speak(response.msg, {
            androidParams: {
              KEY_PARAM_PAN: -1,
              KEY_PARAM_VOLUME: 0.5,
              KEY_PARAM_STREAM: 'STREAM_MUSIC',
            },
          });
          navigation.navigate('language-success');
        }
        if (response.flag == 'search-success') {
          setResData(response);
          setAvailability([...availability, response.item]);
          Tts.speak(response.msg, {
            androidParams: {
              KEY_PARAM_PAN: -1,
              KEY_PARAM_VOLUME: 0.5,
              KEY_PARAM_STREAM: 'STREAM_MUSIC',
            },
          });
        } else {
          Tts.speak(response.msg, {
            androidParams: {
              KEY_PARAM_PAN: -1,
              KEY_PARAM_VOLUME: 0.5,
              KEY_PARAM_STREAM: 'STREAM_MUSIC',
            },
          });
        }
      })
      .catch((err) => console.error(err));
  };

  const readShop = function(shop_id) {
    var msg="";
    
    for (var i=0; i < availability.length; i++) {
      if (availability[i].shop_id == shop_id) {
        msg += "Shop "+availability[i].shop_name+" has an availability of "+(availability[i].perc*100)+"% of the total list";

        Tts.speak('Availaibility of the Products from the chosen shop is as follows.\n'+msg, {
          androidParams: {
            KEY_PARAM_PAN: -1,
            KEY_PARAM_VOLUME: 0.5,
            KEY_PARAM_STREAM: 'STREAM_MUSIC',
          },
        });
      }
    }
  }

  const selectShop = function (shop_id) {
    // Get Items for the Shop Only and send to Next UI
    var shop = null;
    for (var i = 0; i < availability.length; i++) {
      if (availability[i].shop_id == shop_id) {
        shop=availability[i]
      }
    }

    if (shop != null) {
      navigation.navigate('voiceSearchResults', shop)
    }
  }

  return (
    <LoadingActionContainer fixed>
      <Container
        style={{
          padding: 10,
          flex: 1
        }}>

        <ScrollView style={{height: '75%'}}>
          {availability ? availability.map((item) => {
            return (
            <Card style={{marginTop: 10}} key={item.shop_id} onPress={() => readShop(item.shop_id)} onLongPress={() => selectShop(item.shop_id)}>
              <Card.Content>
                <View style={{flex: 1, flexDirection: 'row'}}>
                  <View style={{
                        flexGrow: 0.25,
                        padding: 5,
                        justifyContent: 'center'
                    }}>
                      <IconX
                        style={{marginBottom: 5}}
                        origin={ICON_TYPE.FONT_AWESOME}
                        name={'shopping-basket'}
                        color={theme.colors.primary}
                      />
                  </View>
                  <View style={{
                    flexGrow: 0.75,
                    padding: 5
                  }}>
                    <Title style={{fontSize: 16}}>{item.shop_name}</Title>
                    <Paragraph style={{margin: 5, fontSize: 12}} accessibile={true} accessibilityRole="text" accessibilityLabel={`Availability from Shop ${item.shop_name} is ${item.perc}%`}>
                      This Shop has {item.perc}% of items in your list.
                    </Paragraph>
                  </View>
                </View>
              </Card.Content>
            </Card>)
            }
          ) : 
          <Text style={{marginTop: 10, fontSize: 12}} accessibile={true} accessibilityRole="text" accessibilityLabel={`No Items or shops are not available`}>No Items or Shosp are not available.</Text>
        }
        </ScrollView>

        <View style={{flexGrow: 1, alignItems: 'center'}}>
          <TouchableOpacity
            style={{width: '100%'}}
            onPress={record}
            accessible={true}
            accessibilityLabel="Tap me to Speak"
            accessibilityHint="Start talking to Select an Option"
            accessibilityRole="button"
          >
            <View
              style={{
                alignItems: 'center',
                padding: 10,
                marginTop: 20,
                backgroundColor: theme.colors.primary,
                borderRadius: 10,
              }}>
              <IconX name={'md-mic'} style={{color: '#fff'}} />
            </View>
          </TouchableOpacity>
        </View>
        <View style={{flexGrow: 1, alignItems: 'center'}}>
          <ButtonX
            style={{width: '100%'}}
            dark={true}
            color={theme.colors.primary}
            onPress = {() => Tts.speak('Alter the Created List and Search again')}
            onLongPress = {() => navigation.navigate('voiceSearchList', availability)}            
            label={'Alter'}
            accessibile={true}
            accessibilityLabel={`Alter the Created List`}
            accessibilityHint={`Go back to the Initial List Creation to Edit the Created List`}
          />
        </View>
        
      </Container>
    </LoadingActionContainer>
  );
};

export default MainScreen;
