/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.jena.sparql.sse;

import org.apache.jena.sparql.ARQException;

public class SSE_Exception extends ARQException {
    public SSE_Exception(String msg, Throwable cause)    { super(msg, cause) ; }
    public SSE_Exception(String msg)                     { super(msg) ; }
    public SSE_Exception(Throwable cause)                { super(cause) ; }
    public SSE_Exception()                               { super() ; }
}
