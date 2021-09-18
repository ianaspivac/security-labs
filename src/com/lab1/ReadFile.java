package com.lab1;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.List;

public class ReadFile {
    //inlineFlag = 1 variable
    //inlineFlag = 2 value
    int quotes = 1;
    int inlineFlag = 1;
    String keyWord = "";
    String closingKeyWord = "";
    boolean prevLineKeyword = false;
    boolean prevLineClosing = false;

    public List<String> readFile(String filename) {
        List<String> records = new ArrayList<String>();
        try {
            BufferedReader reader = new BufferedReader(new FileReader(filename));
            String[] path = filename.split("\\.audit");
            BufferedWriter fileCreate = new BufferedWriter(new FileWriter(path[0] + ".json"));
            fileCreate.write("{");
            fileCreate.close();
            BufferedWriter writer = new BufferedWriter(new FileWriter(path[0] + ".json", true));
            String line;
            while ((line = reader.readLine()) != null) {
                //if it's a comment
                if (!line.isEmpty()) {
                    if (line.charAt(0) == '#' && quotes != -1) {
                        continue;
                    }
                }
                if (line.isEmpty()) {
                    continue;
                }
                //if the string ends on other line
                if (quotes == -1) {
                    for (int i = 0; i < line.length(); i++) {
                        writer.append(line.charAt(i));
                        if (line.charAt(i) == '\\') {
                            writer.append('"');
                        }
                        if (line.charAt(i) == '"') {
                            quotes = 1;
                            break;
                        }
                    }
                }//if keyword inside contains a variable with a value
                else if (line.contains("<") && !line.contains("</") && line.trim().contains("type")) {
                    String tempKeyWord = "";
                    int i = 1;
                    String trimLine = line.trim();
                    while (trimLine.charAt(i) != '_') {
                        if (trimLine.charAt(i) == ' ') {
                            break;
                        }
                        tempKeyWord += trimLine.charAt(i);
                        i++;
                    }

                    if (tempKeyWord.equals(keyWord) && keyWord.equals(closingKeyWord)) {
                        writer.append("}");
                        prevLineClosing = true;
                    } else if (!keyWord.equals(tempKeyWord) && keyWord.equals(closingKeyWord) && !prevLineKeyword && !line.contains("check_type")) {
                        writer.append("}]");
                        prevLineClosing = true;
                    } else {
                        prevLineClosing = false;
                    }
                    if (prevLineClosing) {
                        writer.append(",");
                    }
                    if (tempKeyWord.equals(keyWord)) {
                        writer.append("{");
                    } else {
                        writer.append('"' + tempKeyWord + '"' + ":[{");
                    }

                    while (trimLine.charAt(i) != ':') {
                        i++;
                    }
                    i++;
                    writer.append('"' + "type" + '"' + ":");
                    while (i < trimLine.length() - 1) {
                        writer.append(trimLine.charAt(i));
                        i++;
                    }
                    keyWord = tempKeyWord;
                    writer.append(",");
                    prevLineKeyword = true;
                }//if it's opening keyword
                else if (!line.contains("</") && line.contains("<") && !line.trim().contains(" ")) {

                    String tempKeyWord;
                    tempKeyWord = line.trim();
                    tempKeyWord = tempKeyWord.substring(1, tempKeyWord.length() - 1);
                    if (tempKeyWord.equals(keyWord) && keyWord.equals(closingKeyWord)) {
                        writer.append("}");
                        prevLineClosing = true;
                    } else if (!keyWord.equals(tempKeyWord) && !prevLineKeyword) {
                        writer.append("}]");
                        prevLineClosing = true;
                    } else {
                        prevLineClosing = false;
                    }
                    if (!tempKeyWord.equals(keyWord)) {
                        keyWord = tempKeyWord;
                        if (prevLineClosing) {
                            writer.append(",");
                        }
                        writer.append('"' + keyWord + '"' + ":[{");
                    } else {
                        writer.append(",{");
                    }
                    prevLineKeyword = true;
                    // prevLineClosing = false;
                }//if it's closing keyword
                else if (line.contains("</")) {
                    String tempClosingKeyWord;
                    tempClosingKeyWord = line.trim();
                    tempClosingKeyWord = tempClosingKeyWord.substring(2, tempClosingKeyWord.length() - 1);
                    if ((!keyWord.equals(tempClosingKeyWord) || (prevLineClosing && closingKeyWord.equals(keyWord)) && !prevLineKeyword)
                    ) {
                        writer.append("}]");
                        prevLineClosing = true;
                    } else {
                        prevLineClosing = false;
                    }
                    closingKeyWord = tempClosingKeyWord;
                    prevLineKeyword = false;

                }//if it's content inside <> </>
                else if (!line.contains("<")) {
                    if (!line.isEmpty()) {
                        if (!prevLineKeyword) {
                            writer.append(",");
                        }
                        writer.append('"');
                    }
                    for (int i = 0; i < line.length(); i++) {

                        if (line.charAt(i) == '"') {
                            quotes *= -1;
                            continue;
                        }
                        if (line.charAt(i) != ':' && inlineFlag != 2 && line.charAt(i) != ' ') {
                            writer.append(line.charAt(i));
                        } else if (line.charAt(i) == ':' && inlineFlag != 2) {
                            inlineFlag = 2;
                            writer.append('"' + ":" + '"');
                        } else if (inlineFlag == 2) {
                            writer.append(line.charAt(i));
                            if (line.charAt(i) == '\\') {
                                writer.append('"');
                            }
                        }
                    }
                    if (quotes != -1 && !line.isEmpty()) {
                        writer.append('"');
                    }
                    inlineFlag = 1;
                    prevLineKeyword = false;
                    prevLineClosing = false;
                }
                if (quotes != -1) {
                    writer.append("\n");
                }
                records.add(line);
            }
            writer.append("}]}");
            reader.close();
            writer.close();
            return records;
        } catch (Exception e) {
            System.err.format("Exception occurred trying to read '%s'.", filename);
            e.printStackTrace();
            return null;
        }
    }
}
