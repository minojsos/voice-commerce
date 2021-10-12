/* eslint-disable react-native/no-inline-styles */
import React, {useEffect, useContext, useState} from 'react';
import {View, SafeAreaView, TextInput, Text, ScrollView, TouchableOpacity} from 'react-native';
import LoadingActionContainer from '../../Components/LoadingActionContainer';
import {ButtonX, Container} from '../../Components';
import NavigationStyles from '../../Styles/NavigationStyles';
import useAppTheme from '../../Themes/Context';
import { Avatar, Button, Card, Title, Paragraph } from 'react-native-paper';
import {IconX, ICON_TYPE} from '../../Icons';
import AudioRecord from 'react-native-audio-record';
import {BASE_URL} from '../../Config/index';
import Tts from 'react-native-tts';
// import { Voice } from 'react-native-voice';
import { LocalizationContext } from '../../Translations';
import { Voice } from '@react-native-voice/voice';

const MainScreen = ({navigation}) => {
  const {theme} = useAppTheme();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [address, setAddress] = useState('');
  const [phone, setPhone] = useState('');

  const [language, setLanguage] = useState('en');
  const [languageTts, setLanguageTts] = useState('en-IN');
  const [locale, setLocale] = useState('en_us');
  const [isRecording, setIsRecording] = useState(false);

  const LISTEN_COMMAND_EN = "begin"
  const LISTEN_COMMAND_TA = "தொடங்க"

  const {
    translations,
  } = useContext(LocalizationContext);

  const updateProfile = () => {

  }

  useEffect(() => {
    Voice.onSpeechStart = onSpeechStart()
    Voice.onSpeechRecognized = onSpeechRecognized()
    Voice.onSpeechResults = onSpeechResults()

    Tts.speak(translations['myProfileTts'], {
      androidParams: {
        KEY_PARAM_PAN: -1,
        KEY_PARAM_VOLUME: 0.5,
        KEY_PARAM_STREAM: 'STREAM_MUSIC',
      },
    });

    // const newData = JSON.parse(response.orders);
    // setListData(newData);
    // for (let value of newData) {
    //   // for (let value of searchData.list) {
    //   Tts.speak(`address${value.address}`, {
    //     androidParams: {
    //       KEY_PARAM_PAN: -1,
    //       KEY_PARAM_VOLUME: 0.5,
    //       KEY_PARAM_STREAM: 'STREAM_MUSIC',
    //     },
    //   });
    //   // Tts.speak(`cancel_reason${value.cancel_reason}`, {
    //   //   androidParams: {
    //   //     KEY_PARAM_PAN: -1,
    //   //     KEY_PARAM_VOLUME: 0.5,
    //   //     KEY_PARAM_STREAM: 'STREAM_MUSIC',
    //   //   },
    //   // });
    // }
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
  }, []);

  const record = () => {
    console.log('record');

    AudioRecord.start();
    timeout;
    let timeout = setTimeout(() => {
      stopRecord();
      console.log('hello');
    }, 5000);
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
    formData.append('flag', 'name');
    formData.append(orderId, 1);
    console.log(formData);

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
          Tts.speak(response.msg, {
            androidParams: {
              KEY_PARAM_PAN: -1,
              KEY_PARAM_VOLUME: 0.5,
              KEY_PARAM_STREAM: 'STREAM_MUSIC',
            },
          });
          navigation.navigate('order-menu');
        }
        if (!response.flag === 'navigation-error') {
          navigation.navigate(response.flag);
        } else {
          console.log('route error');
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
      if (menuitem.includes("username") || menuitem.includes("பயனர்பெயர்")) {
        var list = menuitem.split("username")
        if (list.length > 1 && list[1] != "") {
          setUsername(list[1])
        }
      } else if (menuitem.includes("email") || menuitem.includes("மின்னஞ்சல்")) {
        var list = menuitem.split("email")
        if (list.length > 1 && list[1] != "") {
          setEmail(list[1])
        }
      } else if (menuitem.includes("address") || menuitem.includes("முகவரி")) {
        var list = menuitem.split("address")
        if (list.length > 1 && list[1] != "") {
          setAddress(list[1])
        }
      } else if (menuitem.includes("phone") || menuitem.includes("தொலைபேசி")) {
        var list = menuitem.split("phone")
        if (list.length  > 1 && list[1] != "") {
          setPhone(phone[1])
        }
      } else if (menuitem.includes("go back") || menuitem.includes("திரும்பி செல்")) {
        navigation.navigate('assistant');
      }

      setIsRecording(false)
    }
  }

  return (
    <LoadingActionContainer fixed>
      <Container
        style={{
          padding: 10,
        }}>
          <ScrollView>
            <Card 
            style={{display: 'flex', justifyContent: 'space-between', flexDirection: 'row', width: '100%', marginTop: 10}}
            accessible={true}
            accessibilityLabel={translations['editProfileLabel']}
            accessibilityHint={translations['editProfileLabelHint']}
            >
              <Card.Content>
                <Card style={{padding:5, margin:10}}>
                <Text accessible={true} accessibilityLabel={translations['usernameText']}>{translations['usernameText']}</Text>
                <TextInput
                  onChangeText={setUsername}
                  value={username}
                  accessible={true}
                  accessibilityLabel={translations['usernameText']}
                  accessibilityHint={translations['usernameTextHint']}
                  // accessibilityValue={username}
                  placeholder="Username"
                  keyboardType="text"
                />
                </Card>

                <Card style={{padding:5, margin:10}}>
                <Text accessible={true} accessibilityLabel={translations['emailText']}>{translations['emailText']}</Text>
                <TextInput
                  onChangeText={setEmail}
                  value={email}
                  accessible={true}
                  accessibilityLabel={translations['emailText']}
                  accessibilityHint={translations['emailTextHint']}
                  // accessibilityValue={username}
                  placeholder="Email"
                  keyboardType="text"
                />
                </Card>
                
                <Card style={{padding:5, margin:10}}>
                <Text accessible={true} accessibilityLabel={translations['addressText']}>{translations['addressText']}</Text>
                <TextInput
                  onChangeText={setAddress}
                  value={address}
                  accessible={true}
                  accessibilityLabel={translations['addressText']}
                  accessibilityHint={translations['addressTextHint']}
                  // accessibilityValue={username}
                  placeholder="Address"
                  keyboardType="text"
                />
                </Card>
                
                <Card style={{padding:5, margin:10}}>
                <Text accessible={true} accessibilityLabel={translations['phoneText']}>{translations['phoneText']}</Text>
                <TextInput
                  onChangeText={setPhone}
                  value={phone}
                  accessible={true}
                  accessibilityLabel={translations['phoneText']}
                  accessibilityHint={translations['phoneTextHint']}
                  // accessibilityValue={phone}
                  placeholder="Phone"
                  keyboardType="text"
                />
                </Card>

                <ButtonX
                  label={translations['updateProfileButton']}
                  accessible={true}
                  accessibilityLabel={translations['updateProfileButtonHint']}
                  accessibilityHint={translations['updateProfileButtonHint']}
                  accessibilityRole="button"
                  dark={true}
                  onPress={() => Tts.speak(translations['updateProfileButtonHint'])}
                  onLongPress={() => updateProfile()}
                />
              </Card.Content>
            </Card>
        </ScrollView>

        <View style={{alignItems: 'center'}}>
          <TouchableOpacity
            style={{width: '100%'}}
            onPress={record}
            accessible={true}
            accessibilityLabel={translations['micLabel']}
            accessibilityHint={translations['micMenuLabel']}
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
      </Container>
    </LoadingActionContainer>
  );
};

MainScreen.navigationOptions = ({navigation, screenProps}) => {
  const {theme} = screenProps;
  return {
    headerStyle: [
      NavigationStyles.header_statusBar,
      {backgroundColor: theme.colors.header},
    ],
    headerTitle: 'Profile',
    headerTintColor: theme.colors.headerTitle,
    headerTitleStyle: [
      NavigationStyles.headerTitle,
      {color: theme.colors.headerTitle},
    ],
  };
};

export default MainScreen;
