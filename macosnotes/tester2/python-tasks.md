<div><b>Creation Date:</b> Thursday, January 11, 2018 at 1:57:48 PM<br></div>
<div><b>Modification Date:</b> Friday, May 18, 2018 at 10:41:11 AM<br></div>
<div><span style="font-size: 17px">PYTHON tasks</span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px">Vital role of humans in machine learning talk. CTO conference. Look it up</span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px">Pix2code</span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px">GAN Hacks. </span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px"><br></span></div>
<div>sudo git branch -D gb_longranger</div>
<div>sudo git push origin —delete remotes/origin/gb_longranger</div>
<div><br></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px">yield and generators - </span><font color="#DCA00D"><span style="font-size: 13px">https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do</span></font><font color="#DCA00D"><span style="font-size: 13px"><br></span></font></div>
<div><span style="font-size: 17px">send</span></div>
<div><span style="font-size: 17px">itertools</span></div>
<div><span style="font-size: 17px">packages</span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px">list comprehensions:</span></div>
<div><span style="font-size: 16px">If you used to do it like this:</span></div>
<div><span style="font-size: 16px">new_list = []</span></div>
<div><span style="font-size: 16px">for i in old_list:</span></div>
<div><span style="font-size: 16px">    if filter(i):</span></div>
<div><span style="font-size: 16px">        new_list.append(expressions(i))</span></div>
<div><span style="font-size: 16px">You can obtain the same thing using list comprehension:</span></div>
<div><b><span style="font-size: 16px">new_list = [expression(i) for i in old_list if filter(i)]</span></b><span style="font-size: 13px"><br></span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px">classes and __init__ and self especially if diff from php</span></div>
<div><span style="font-size: 17px">	all methods take self as first param</span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px">gather and scatter of *args </span></div>
<div><span style="font-size: 17px">also **kwargs</span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px">set — gets just the unique items. so simple way to find uniques in a list:</span></div>
<div><span style="font-size: 17px">	set([1,1,1,1,2,2,2,3,3,3])</span></div>
<div><span style="font-size: 17px">	will equal {1,2,3}</span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px">virtual environments!</span></div>
<div><span style="font-size: 17px">	conda create —name NAMEHERE libs</span></div>
<div><span style="font-size: 17px">	condo create —name numpytest numpy</span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px">matplotlib</span></div>
<div><span style="font-size: 17px">numpy</span></div>
<div><span style="font-size: 17px">scikit</span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px">pandas/plotly — merging from two diff data sources, matched on something like country code, say you wanna add population to power consumption data frame so you can do power usage per capita, for example. some sort of </span></div>
<div><span style="font-size: 17px">df1[“popsize”] = df2[“popsize”].where(df[‘country’]==df2[“country”])</span></div>
<div><span style="font-size: 17px">or just do it straight regular python funcs()??</span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px">pandas find in a very long row where value of iloc[X] == Y or !=Y, etc</span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px">what is the best json encoder decoder?</span></div>
<div><span style="font-size: 17px">import json</span></div>
<div><span style="font-size: 17px">json.dump() # go from dict to str (“serialize object”) with FILE</span></div>
<div><span style="font-size: 17px">son.dumps() # same but with STRING</span></div>
<div><span style="font-size: 17px">json.load() #go from str to json</span></div>
<div><span style="font-size: 17px">json.loads()</span></div>
<div><br></div>
<div><span style="font-size: 18px">load = with file | loads = with string</span><br></div>
<div><span style="font-size: 17px">The json.loads function does not take the file path, but the file contents as a string</span><span style="font-size: 22px"><br></span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><font color="#DCA00D"><span style="font-size: 17px">https://www.youtube.com/watch?v=vGphzPLemZE</span></font><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px">deploy options:</span></div>
<div><span style="font-size: 17px">ngrok</span></div>
<div><span style="font-size: 17px">heroku (w gunicorn)</span></div>
<div><span style="font-size: 17px">AWS lambda (“server less”) used via the wrapper Zappa</span></div>
<div><span style="font-size: 17px">google compute engines (an example of a fully controllable virtual machine)</span></div>
<div><span style="font-size: 17px">docker</span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px">sample project:</span></div>
<div><span style="font-size: 17px">run thru diff permutations of averaged mean = actual mean, with random numbers, and then a sliding scale of how many sample and how many runs of those samples and how closely that relates to actually sampling ALL the numbers.</span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px">example: use random.sample(pop,k) to get k length list from the population.</span></div>
<div># Pick 10 random images</div>
<div>sample_indexes = random.sample(range(len(images32)), 10)</div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px">so if you have 10 random numbers and the mean is 7.3, how many Xnums.mean() x runs before you get to some very close to 7.3 result… and how does that scale for 1000 numbers, and i guess related to the range in those numbers, percent that are outliers… etc. what diff makes an outlier (outside the 90%) etc. too bad i don’t know the names of these characteristics!</span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px">how many characters in novels by genre, poetry, plays, movies.</span></div>
<div><span style="font-size: 17px">correlated to stars on rotten tomatoes or amazon sales rank or all time copies, etc.</span></div>
<div><span style="font-size: 17px">so you can say, i m writing  pulp fiction and need 4 characters and 3 sub-characters, etc.</span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px">MACHINE LEARNING -definitions from https://developers.google.com/machine-learning/glossary/</span></div>
<ol>
<li><span style="font-size: 17px">generalized linear model</span></li>
<li><span style="font-size: 17px">regression = continuous (floating point) values v classification = enumed [a | b | c |…n] </span></li>
<li><span style="font-size: 17px">L2 and L1 regularization </span></li>
<li><span style="font-size: 17px">softmax (makes sense) v candidate sampling (which just work by dropping some negatives?)</span></li>
<li><span style="font-size: 17px">dense layers makes sense, what of convolutional (</span><font color="#DCA00D">https://www.tensorflow.org/tutorials/layers</font><span style="font-size: 17px">)</span></li>
<li><span style="font-size: 17px">logits (</span><font color="#DCA00D">https://stackoverflow.com/questions/41455101/what-is-the-meaning-of-the-word-logits-in-tensorflow</font><span style="font-size: 17px">)</span></li>
<li><span style="font-size: 17px">numpy</span></li>
<li><span style="font-size: 17px">scikit-learn</span></li>
<li><span style="font-size: 17px">pandas</span></li>
<li><span style="font-size: 17px">tensorflow</span></li>
</ol>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px">weighted arithmetic mean vs geometric mean (v standard arithmetic mean)</span></div>
<div><span style="font-size: 17px"><br></span></div>
<div><span style="font-size: 17px">May meetup</span></div>
<div><span style="font-size: 17px">Pyviz.org</span><span style="font-size: 17px"> site</span></div>
<div><span style="font-size: 17px">Marries python to JavaScript </span></div>
<div><span style="font-size: 17px">DASK for giant data</span></div>
<div><span style="font-size: 17px">Bokeh server app to. Serve html</span></div>
<div><span style="font-size: 17px"><br></span></div>

