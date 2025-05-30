# Class to represent an Android Method
class AndroidMethod:
	# Constructor to initialize the AndroidMethod object
	def __init__(self, sha256, signature, documentation):
		self.sha256		    = sha256
		self.signature      = signature
		self.documentation  = documentation

	# Function to print the key in a formatted way with emojis
	def __str__(self):
		return (
				"--- 🔑 SHA256		 : {}\n"
				"--- 📌 Signature	 : {}\n"
				"--- 📚 Documentation: \n{}\n"
				.format(self.sha256, self.signature, self.documentation)
		)
	
	# Add signature
	def addSignatureToPrompt(self, promptBase):
		if self.signature:
			promptBase += "\n\n**Method Signature:**\n" + self.signature
		return promptBase
	
	# Add documentation
	def addDocumentationToPrompt(self, promptBase):
		if self.documentation:
			promptBase += "\n\n**Method Documentation:**\n" + self.documentation
		return promptBase

	# Add signature, documentation and source code
	def addAllToPrompt(self, promptBase):
		promptBase = self.addSignatureToPrompt(promptBase)
		promptBase = self.addDocumentationToPrompt(promptBase)
		return promptBase

# Function to iterate over each method and classify it N times
def labelAndroidMethod(llmInterface, prompt, possibleLabels, NUM_REPLIES, MAX_THRESHOLD):
	
	# Initialize a dictionary to store the frequency of each label
	labelFrequency = {}

	# Send the request N times or until the MAX_THRESHOLD is reached
	for attempts in range(MAX_THRESHOLD):
		# Initialize a counter for the number of valid replies
		numAttempts = sum(labelFrequency.values())
		
		# If number of replies is satisfied, break
		if numAttempts >= NUM_REPLIES:
			break
		
		# Send request to the LLM
		predictedLabel = llmInterface.sendRequest(prompt).strip().upper().replace("*", "")

		# Test purposes
		# print(predictedLabel)

		# Check if the predicted label is valid
		if predictedLabel in possibleLabels:
			if predictedLabel in labelFrequency:
				labelFrequency[predictedLabel] += 1
			else:
				labelFrequency[predictedLabel] = 1

	# if the maximum threshold is reached, add a NONE label
	if attempts == MAX_THRESHOLD-1:
		print("--- ❌ Maximum attempts reached. Skipping to the next one.")	
		labelFrequency["MAX_RETRY"] = NUM_REPLIES
	
	return labelFrequency

# Function to get the most frequent label
def getMostFrequentLabel(freqDict):
	return max(freqDict, key=freqDict.get)