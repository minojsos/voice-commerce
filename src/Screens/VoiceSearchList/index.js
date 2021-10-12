/* eslint-disable react-native/no-inline-styles */
import React, {useEffect, useContext, useState} from 'react';
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
import {LocalizationContext} from '../../Translations';
import { Voice } from '@react-native-voice/voice';

const MainScreen = ({routes, route, navigation}) => {
  const {theme} = useAppTheme();
  const [language, setLanguage] = useState('en');
  const [languageTts, setLanguageTts] = useState('en-IN');

  // eslint-disable-next-line prettier/prettier
  const {username, password} = useStoreState((state) => ({
    username: state.login.username,
    password: state.login.password,
  }));
  const [resData, setResData] = useState('');
  const [searchList, setSearchList] = useState(route.params);
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

    // Load the Chosen Language
    setLanguage(AsyncStorage.getItem('language'))

    if (language == 'ta') {
      setLanguageTts('ta-IN')
    } else {
      setLanguageTts('en-IN')
    }

    const _toggleDrawer = () => {
      navigation.toggleDrawer();
    };
    Tts.speak(
      translations['voiceSearchTts'],
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
        // Read the List
        readList()
      } else if (menuitem.includes("continue") || menuitem.includes("தொடரும்")) {
        // Check/Predict Availability Against Shops        
        let formData = new FormData();

        var url=""
        if (language=="ta") {
          url='/predictAvailability'
          formData.append('language', 'ta')
        } else {
          url='/predictAvailability'
          formData.append('language', 'en')
          formData.append('list', searchList)
        }

        fetch(`${BASE_URL}${url}`, {
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
            navigation.navigate('orderAvailability', response.data)
          })
          .catch((err) => console.error(err));
      } else if (menuitem.includes("go back") || menuitem.includes("திரும்பி செல்")) {
        navigation.navigate('language-success');
      }

      setIsRecording(false)
    }
  }

  useEffect(() => {
    if (language == 'ta') {
      setLanguageTts('ta-IN')
    } else {
      setLanguageTts('en-IN')
    }

    AsyncStorage.setItem('language', language);
  }, [language]);

  const record = () => {
    console.log('record');

    setSearchList(cartitems)

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
    // formData.append('userId', await AsyncStorage.getItem('userId'));

    var url=""
    if (language=="ta") {
      url='/predictAvailability'
      formData.append('language', 'ta')
    } else {
      url='/predictAvailability'
      formData.append('language', 'en')
    }

    fetch(`${BASE_URL}${url}`, {
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
          setSearchList([...searchList, response.item]);
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

  return (
    <LoadingActionContainer fixed>
      <Container
        style={{
          padding: 10,
          flex: 1,
        }}>
        

        <ScrollView style={{height: '60%'}}>
          {searchList ? searchList.map((item) => {
          return (
            <Card style={{marginTop: 10}} key={item._id}>
              <Card.Content>
                <View style={{flex: 1, flexDirection: 'row'}}>
                  <View style={{
                    justifyContent: 'center',
                    flexGrow: 0.1
                  }}>
                    <IconX
                      style={{marginBottom: 5}}
                      origin={ICON_TYPE.FONT_AWESOME}
                      name={'circle-o'}
                      color={theme.colors.primary}
                    />
                  </View>
                  <View style={{
                        flexGrow: 0.4,
                    }}>
                      <Paragraph style={{textAlign: 'left'}}>
                        <Text style={{fontSize: 16, textTransform: 'capitalize', textDecorationStyle: 'solid'}} accessibile={true} accessibilityLabel={item.item_name} accessibilityHint={`This is an item ${item.item_name} with quantity ${item.item_qty}  ${item.item_unit}`} accessibilityRole="text">
                          {item.item_name}{"\n"}
                        </Text>
                        <Text style={{fontSize: 12}}>
                          {item.item_qty}{item.item_unit}
                        </Text>
                      </Paragraph>
                  </View>
                  
                  <View style={{
                        flexGrow: 0.4,
                        padding: 5
                    }}>
                      <Paragraph style={{textAlign: 'center'}}>
                        {item.item_offer_price != null ?
                        <>
                        <Text accessibile={true} accessibilityLabel={`${item.item_qty}`} accessibilityHint={`This is an item ${item.item_name} with quantity ${item.item_qty} ${item.item_unit}`}>
                          Rs.{item.item_offer_price}/{item.item_unit}{"\n"}
                        </Text>
                        <Text style={{fontSize: 10,textDecorationLine: 'line-through', textDecorationStyle: 'solid'}} accessible={true} accessibilityLabel={`Original Price of ${item.item_name} is Rs.${item.item_rate} and the Offer Price is Rs.${item.item_offer_price}`}>
                          Rs.{item.item_rate}/{item.item_unit}
                        </Text>
                        </>
                        : 
                        <Text accessibile={true} accessibilityLabel={`${item.item_qty}`} accessibilityHint={`This is an item ${item.item_name} with quantity ${item.item_qty} ${item.item_unit}`}>
                          Rs.{item.item_rate}/{item.item_unit}
                        </Text>
                        }
                      </Paragraph>
                  </View>

                  <View style={{
                        flexGrow: 0.2,
                        padding: 5
                    }}>
                      <IconX
                        style={{marginBottom: 5, alignItems: 'center', justifyContent: 'center'}}
                        origin={ICON_TYPE.FONT_AWESOME}
                        name={'times'}
                        color={theme.colors.primary}
                      />
                  </View>
                </View>
              </Card.Content>
            </Card>)}
          ) : null}
        </ScrollView>

        <View style={{flex: 1, flexDirection: 'row', justifyContent: 'center'}}>
          <View style={{flexGrow: 1, alignItems: 'center'}}>
            <TouchableOpacity
              style={{width: '100%'}}
              onPress={record}
              accessible={true}
              accessibilityLabel={translations['micLabel']}
              accessibilityHint={translations['micMenuVoiceSearch']}
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
        </View>
        <View style={{flex: 1, flexDirection: 'row', justifyContent: 'space-around'}}>
          <View style={{flexGrow: 0.25, alignItems: 'center'}}>
            <ButtonX
              // loading={loading}
              dark={true}
              color={theme.colors.primary}
              onPress = {() => Tts.speak(translations['btnAlterLongPress'])}
              onLongPress={() => navigation.navigate('voice-search', searchList)}            
              label={translations['btnAlter']}
              accessibile={true}
              accessibilityLabel="Alter Search List"
              accessibilityHint="Long Press to Go Back and Alter Search List"
              accessibilityRole="button"
            />
          </View>

          <View style={{flexGrow: 0.25, alignItems: 'center'}}>
            <ButtonX
              // loading={loading}
              dark={true}
              color={theme.colors.primary}
              label={translations['btnSearch']}
              onPress = {() => Tts.speak(translations['btnAvailabilityLongPress'])}
              onLongPress={() => navigation.navigate('orderAvailability', searchList)}
              accessibile={true}
              accessibilityLabel="Search using List"
              accessibilityHint="Long Press to Search for Items using List against shops"
              accessibilityRole="button"
            />
          </View>
          
          <View style={{flexGrow: 0.25, alignItems: 'center'}}>
            <ButtonX
              // loading={loading}
              dark={true}
              color={theme.colors.primary}
              onPress = {() => Tts.speak(translations['btnReadLongPress'])}
              onLongPress={() => readList()}
              label={translations['btnRead']}
              accessibile={true}
              accessibilityLabel="Read Search List"
              accessibilityHint="Long Press to Read Search List"
              accessibilityRole="button"
            />
          </View>
        </View>

      </Container>
    </LoadingActionContainer>
  );
};

export default MainScreen;
