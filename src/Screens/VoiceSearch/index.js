/* eslint-disable react-native/no-inline-styles */
import React, {useEffect, useContext, useState} from 'react';
import {View, Text, ScrollView, Alert} from 'react-native';
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
import { readFileAssets } from 'react-native-fs';
import AsyncStorage from '@react-native-community/async-storage';
import {LocalizationContext} from '../../Translations';
import { Voice } from '@react-native-voice/voice';

const MainScreen = ({routes, navigation}) => {
  const {theme} = useAppTheme();
  const [language, setLanguage] = useState('en')
  const [languageTts, setLanguageTts] = useState('en-IN')

  // eslint-disable-next-line prettier/prettier
  const {username, password} = useStoreState((state) => ({
    username: state.login.username,
    password: state.login.password,
  }));
  const [resData, setResData] = useState('');
  const [allItems, setAllItems] = useState([]);
  const [inputItemName, setInputItemName] = useState('');
  const [inputItemQty, setInputItemQty] = useState('');
  const [isRecording, setIsRecording] = useState(false);

  const LISTEN_COMMAND_EN = "begin"
  const LISTEN_COMMAND_TA = "தொடங்க"

  const loadData = () => {
    const image_search = []// await AsyncStorage.getItem('@image_search');
    if (image_search.length > 0) {
      for (var i = 0; i < image_search.length; i++) {
        if (!isNaN(image_search[i].item_qty) && image_search[i].item_qty > 0) {
          var item = {"_id":i, "item_name": image_search[i].item_name, "item_qty": image_search[i].item_qty, "item_unit": "kg"};
          setAllItems([...allItems, item]);
        }
      }
    } else {
      var item = null;
      var item = {"_id": 15, "item_name": "banana", "item_qty": 75.0, "item_unit":"kg", "item_rate":100, "item_offer_price":null}
      setAllItems([...allItems, item]);
      var item = {"_id": 16, "item_name": "banana", "item_qty": 75.0, "item_unit":"kg", "item_rate":100, "item_offer_price":90}
      setAllItems([...allItems, item]);
    }
  }

  const {
    translations
  } = useContext(LocalizationContext);

  useEffect(() => {
    // Load Dummy Data
    loadData()

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
        navigation.navigate('voiceSearchList', allItems)
      } else if (menuitem.includes("alter") || menuitem.includes("மாற்ற")) {
        navigation.navigate('voiceSearchAlter', allItems)
      } else if (menuitem.includes("go back") || menuitem.includes("திரும்பி செல்")) {
        navigation.navigate('language-success');
      }

      setIsRecording(false)
    }
  }

  const record = () => {
    Tts.speak(translations['startingRecordingTts'])
    AudioRecord.start();
    timeout;
    let timeout = setTimeout(() => {
      stopRecord();
    }, 8000);
  };

  const stopRecord = async () => {
    const audioFile = await AudioRecord.stop();
    AudioRecord.on('data', (data) => {});
    Tts.speak(translations['stoppingRecordingTts'])
    console.log('Recording Stopped: audioFile 🍷', audioFile);
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

    var url = ""
    if (language == 'ta') {
      url = "/voicesearch/ta"
    } else {
      url = "/voicesearch/en"
    }
    var url = 
    fetch(`${BASE_URL}${url}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((response) => {
        console.log(response);

        // Iterate Response and Add/Edit/Delete item from list
        var name = response.result.name;
        var qty = response.result.qty;
        var action = response.result.action;

        if (action == 1) {
          // Add
          setAllItems([...allItems, {"_id": allItems.length, "item_name": name, "item_qty": qty, "item_unit": "kg"}]);
        } else if (action == 2) {
          // Edit
          for (var i = 0; i < allItems.length; i++) {
            if (allItems[i].item_name == name) {
              var newAllItems = allItems;
              newAllItems[i] = {"_id": i, "item_name": name, "item_qty": qty, "item_unit": "kg"};
              setAllItems(newAllItems)
            }
          }
        } else if (action == 0) {
          // Delete
          var newAllItems = allItems.filter((item) => item.item_name !== name);
          setAllItems(newAllItems)
        }
      })
      .catch((err) => console.error(err));
  };

  const saveList = () => {

  }

  const readList = () => {
    if (allItems.length > 0) {
      for (var i=0; i < allItems.length; i++) {
        Tts.speak(translations.formatString(translations['readListTts'], {item_name: allItems[i].item_name, item_qty: allItems[i].item_qty}))
      }
    } else {
      Tts.speak(translations['noItemsLabel'])
    }
  }

  const addItem = () => {
    var allItemsList = allItems;
    if (inputItemName != "" && inputItemQty.trim() != '' && !isNaN(inputItemQty)) {
      var item = {"_id": allItems.length, "item_name": inputItemName, "item_qty": inputItemQty, "item_unit":"kg"}
      setAllItems([...allItems, item]);
      Alert.alert("Success", translations.formatString(translations['successAddItem'], {itemName: inputItemName, itemQty: inputItemQty}))
    } else {
      Alert.alert("Error", translations['failedAddItem'])
    }
  }

  return (
    <LoadingActionContainer fixed>
      <Container
        style={{
          padding: 10,
          flex: 1,
        }}>

        <ScrollView style={{height: '75%'}}>
          {allItems ? allItems.map((item) => {
          return (
          <Card style={{marginTop: 10}} key={item._id}>
            <Card.Content>
              <View style={{flex: 1, flexDirection: 'row'}}>
                <View style={{
                      flexGrow: 0.5,
                      padding: 5
                  }}>
                    <Text style={{fontSize: 10}}>Name</Text>
                    <Text 
                    accessibile={true}
                    accessibilityHint={`This is an item ${item.item_name} with quantity ${item.item_qty}  ${item.item_unit}`}
                    >
                    {item.item_name}
                    </Text>
                </View>
                
                <View style={{
                      flexGrow: 0.5,
                      padding: 5
                  }}>
                    <Text style={{fontSize: 10}}>Quantity</Text>
                    <Text 
                    accessibile={true}
                    accessibilityHint={`This is an item ${item.item_name} with quantity ${item.item_qty}  ${item.item_unit}`}>
                    {item.item_qty}
                    </Text>
                </View>
              </View>
            </Card.Content>

          </Card>
          )}
          ) : 
          <Text style={{marginTop: 10, fontSize: 12}}>{translations['noItemsLabel']}</Text>
          }

          <View
            style={{
              flex: 1,
              flexDirection: 'row',
              justifyContent: 'space-around',
            }}>
            <View style={{flexGrow: 0.5, alignItems:'center'}}>
              <InputX
                accessible={true}
                accessibilityHint={translations['productNameText']}
                label={translations['productNameLabel']}
                style={{marginTop: 10, backgroundColor: '#fafafa', width: 200}}
                autoCapitalize="none"
                returnKeyType={'next'}
                value={inputItemName}
                onChangeText={setInputItemName}
              />
            </View>
            <View style={{flexGrow: 1, alignItems:'center'}}>
              <InputX
                accessible={true}
                accessibilityHint={translations['productQuantityText']}
                label={translations['productQuantityLabel']}
                style={{marginTop: 10, backgroundColor: '#fafafa', width: 200}}
                autoCapitalize="none"
                returnKeyType={'next'}
                value={inputItemQty}
                onChangeText={setInputItemQty}
              />
            </View>
          </View>
        
        <View
          style={{
            flex: 1,
            flexDirection: 'row',
            justifyContent: 'space-around',
          }}>
          <View style={{flexGrow: 1, alignItems: 'center'}}>
            <TouchableOpacity onPress={record}>
              <View
                style={{
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
            <TouchableOpacity onPress={() => addItem()}>
              <View
                style={{
                  padding: 10,
                  marginTop: 20,
                  backgroundColor: theme.colors.primary,
                  borderRadius: 10,
                }}>
                <IconX name={'md-add'} style={{color: '#fff'}} />
              </View>
            </TouchableOpacity>
          </View>
        </View>
        </ScrollView>
          
        <View style={{flex: 1, flexDirection: 'row', justifyContent: 'space-evenly'}}>
          <View style={{flexGrow: 0.3, alignItems: 'center'}}>
            <ButtonX
            // loading={loading}
            dark={true}
            color={theme.colors.primary}
            onPress = {() => Tts.speak(translations['btnAlterLongPress'])}
            onLongPress = {() => navigation.navigate('voiceSearchAlter', allItems)}
            label={translations['btnAlter']}
            />
          </View>
          <View style={{flexGrow: 0.3, alignItems: 'center'}}>
            <ButtonX
              // loading={loading}
              dark={true}
              color={theme.colors.primary}
              onPress = {() => Tts.speak(translations['btnContinueLongPress'])}
              onLongPress={() => navigation.navigate('voiceSearchList', allItems)}            
              label={translations['btnContinue']}
            />
          </View>
          <View style={{flexGrow: 0.3, alignItems: 'center'}}>
            <ButtonX
              dark={true}
              color={theme.colors.primary}
              onPress = {() => Tts.speak(translations['btnReadLongPress'])}
              onLongPress = {() => readList()}
              label={translations['btnRead']}
            />
          </View>
        </View>
        
      </Container>
    </LoadingActionContainer>
  );
};

export default MainScreen;
